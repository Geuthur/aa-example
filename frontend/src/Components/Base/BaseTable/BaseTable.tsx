// React
import type { ReactNode } from "react";
import { useLocation } from "react-router-dom";

// Third Party
import { flexRender, functionalUpdate, useTable } from "@tanstack/react-table";
import type {
  OnChangeFn,
  PaginationState,
  Row,
  RowData,
  RowSelectionState,
  TableState,
  Updater,
} from "@tanstack/react-table";
import {
  ChevronFirst,
  ChevronLast,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { Button, Form } from "react-bootstrap";
import { useTranslation } from "react-i18next";

// AA Example
import BaseHeader from "@/Components/Base/BaseTable/BaseTableHeader";
import BasePages from "@/Components/Base/BaseTable/BaseTablePages";
import { baseTableFeatures } from "@/Components/Base/BaseTable/tableFeatures";
import type { BaseColumnDef, BaseTableFeatures } from "@/Components/Base/BaseTable/tableFeatures";
import { FetchingLoader } from "@/Components/Base/Loader/FetchingLoader";

// Like v8's InitialTableState: each slice may be given partially (e.g. only pageSize).
export type BaseTableInitialState = {
  [K in keyof TableState<BaseTableFeatures>]?: Partial<TableState<BaseTableFeatures>[K]>;
};

// The server pages the rows: `data` is the current page only and `page` is 1-based.
// A new page size only calls onPageSizeChange, the caller decides which page to show next.
export interface BaseTableServerPagination {
  page: number;
  pageSize: number;
  total: number;
  onPageChange: (page: number) => void;
  onPageSizeChange: (pageSize: number) => void;
  totalText?: string;
}

export interface BaseTableProps<TData extends RowData, TValue = unknown> {
  isFetching?: boolean;
  isLoading?: boolean;
  loadingText?: string;
  serverPagination?: BaseTableServerPagination;
  isError?: boolean;
  debugTable?: boolean;
  striped?: boolean;
  hover?: boolean;
  data?: TData[];
  columns: BaseColumnDef<TData, TValue>[];
  initialState?: BaseTableInitialState;
  exportFileName?: string;
  variant?: "default" | "light";
  emptyText?: string;
  /** Replaces `emptyText` with custom content when there are no rows. */
  emptyState?: ReactNode;
  /** Rendered above the table inside the shell, e.g. buttons or extra filters. */
  toolbar?: ReactNode;
  /** Rendered below the page controls inside the table footer. */
  footer?: ReactNode;
  /** Renders the `footer` of the column definitions as a summary row. */
  showFooter?: boolean;
  /** Extra classes for the shell around table and footer. */
  className?: string;
  /** Extra classes for the `<table>`. */
  tableClassName?: string;
  /** Extra classes for the `<thead>`. */
  headerClassName?: string;
  /** Extra classes for the `<tbody>`. */
  bodyClassName?: string;
  /** Extra classes for every data row; `getRowClassName` adds per-row classes. */
  rowClassName?: string;
  /** Extra classes for the `<tfoot>` summary row (`showFooter`). */
  footClassName?: string;
  /** Extra classes for the footer with page size, status and pagination. */
  footerClassName?: string;
  pageSizeOptions?: number[];
  itemLabel?: string;
  getRowClassName?: (row: Row<BaseTableFeatures, TData>) => string;
  enableFilters?: boolean;
  rowSelection?: RowSelectionState;
  onRowSelectionChange?: OnChangeFn<RowSelectionState>;
  enableRowSelection?: boolean | ((row: Row<BaseTableFeatures, TData>) => boolean);
  getRowId?: (originalRow: TData, index: number, parent?: Row<BaseTableFeatures, TData>) => string;
  onRowClick?: (row: Row<BaseTableFeatures, TData>) => void;
}

const messageCellClass = "aa-table-message text-center py-5 px-3";

const BaseTable = <TData extends RowData, TValue = unknown>({
  isFetching = false,
  isLoading = false,
  loadingText,
  serverPagination,
  isError = false,
  debugTable = false,
  data = [],
  columns,
  initialState = undefined,
  exportFileName = undefined,
  variant = "default",
  emptyText,
  emptyState,
  toolbar,
  footer,
  showFooter = false,
  className,
  tableClassName,
  headerClassName,
  bodyClassName,
  rowClassName,
  footClassName,
  footerClassName,
  pageSizeOptions = [10, 25, 50, 100],
  getRowClassName,
  enableFilters = true,
  rowSelection,
  onRowSelectionChange,
  enableRowSelection,
  getRowId,
  onRowClick,
}: BaseTableProps<TData, TValue>) => {
  const location = useLocation();
  const { t } = useTranslation();

  const serverState = serverPagination && {
    pageIndex: serverPagination.page - 1,
    pageSize: serverPagination.pageSize,
  };

  const table = useTable({
    features: baseTableFeatures,
    data,
    columns,
    getRowId,
    state: {
      ...(rowSelection !== undefined ? { rowSelection } : {}),
      ...(serverState ? { pagination: serverState } : {}),
    },
    // Sorting, filtering and CSV export would only see the current page.
    ...(serverPagination && serverState
      ? {
        manualPagination: true,
        pageCount: Math.max(1, Math.ceil(serverPagination.total / serverPagination.pageSize)),
        enableSorting: false,
        enableColumnFilters: false,
        onPaginationChange: (updater: Updater<PaginationState>) => {
          const next = functionalUpdate(updater, serverState);
          if (next.pageSize !== serverState.pageSize) {
            serverPagination.onPageSizeChange(next.pageSize);
          } else if (next.pageIndex !== serverState.pageIndex) {
            serverPagination.onPageChange(next.pageIndex + 1);
          }
        },
      }
      : {}),
    onRowSelectionChange,
    enableRowSelection,
    debugTable,
    initialState: {
      ...initialState,
      pagination: { pageIndex: 0, pageSize: 15, ...initialState?.pagination },
    } as Partial<TableState<BaseTableFeatures>>,
  });

  const { rows } = table.getRowModel();
  const fileName =
    exportFileName !== undefined ? exportFileName : `ExportedData_${location.pathname}`;

  const isLight = variant === "light";
  const { pageIndex, pageSize } = table.state.pagination;
  const pageCount = table.getPageCount();
  const columnCount = table.getVisibleLeafColumns().length;

  return (
    <div
      className={`aa-table-shell mt-2 ${isLight ? "aa-table-shell-light aa-table-light" : ""} ${className ?? ""}`}
    >
      {toolbar}
      <div
        className={`aa-table-scroll ${isLoading && rows.length > 0 ? "opacity-50 pe-none" : ""}`}
        aria-busy={isLoading}
      >
        <table
          className={`aa-table w-100 text-start ${isLight ? "aa-table-light" : ""} ${tableClassName ?? ""}`}
        >
          <thead className={`aa-table-head ${headerClassName ?? ""}`}>
            <BaseHeader table={table} enableFilters={enableFilters} />
          </thead>
          <tbody className={`aa-table-body ${bodyClassName ?? ""}`}>
            {isError ? (
              <tr>
                <td colSpan={columnCount} className={messageCellClass}>
                  {t("Something went wrong.")}
                </td>
              </tr>
            ) : isLoading && rows.length === 0 ? (
              <tr>
                <td colSpan={columnCount} className={messageCellClass}>
                  <FetchingLoader message={loadingText} />
                </td>
              </tr>
            ) : rows.length === 0 ? (
              <tr>
                <td colSpan={columnCount} className={messageCellClass}>
                  {emptyState ?? emptyText ?? t("No Data Available")}
                </td>
              </tr>
            ) : (
              rows.map((row) => (
                <tr
                  key={row.id}
                  onClick={onRowClick ? () => onRowClick(row) : undefined}
                  className={`aa-table-row ${getRowClassName
                    ? getRowClassName(row)
                    : "aa-table-row-hover"
                    } ${rowClassName ?? ""}`}
                >
                  {row.getVisibleCells().map((cell) => {
                    const meta = cell.column.columnDef.meta as { align?: string } | undefined;
                    const isRight = meta?.align === "right";
                    return (
                      <td
                        key={cell.id}
                        className={`aa-table-cell align-middle ${isRight ? "text-end" : ""}`}
                      >
                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                      </td>
                    );
                  })}
                </tr>
              ))
            )}
          </tbody>
          {showFooter && !isError && rows.length > 0 && (
            <tfoot className={`aa-table-foot ${footClassName ?? ""}`}>
              {table.getFooterGroups().map((footerGroup) => (
                <tr key={footerGroup.id}>
                  {footerGroup.headers.map((header) => {
                    const meta = header.column.columnDef.meta as { align?: string } | undefined;
                    const isRight = meta?.align === "right";
                    return (
                      <td
                        key={header.id}
                        colSpan={header.colSpan}
                        className={`aa-table-cell align-middle ${isRight ? "text-end" : ""}`}
                      >
                        {header.isPlaceholder
                          ? null
                          : flexRender(header.column.columnDef.footer, header.getContext())}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tfoot>
          )}
        </table>
      </div>

      {/* DataTable Footer Controls */}
      <div
        className={`aa-table-footer d-flex flex-column flex-md-row align-items-center justify-content-between gap-3 p-3 ${footerClassName ?? ""}`}
      >
        {/* Page Size Selector, Count Indicator & Export / Status */}
        <div className="d-flex align-items-center justify-content-between gap-3 align-self-stretch align-self-md-auto">
          <div className="d-flex align-items-center gap-3">
            <div className="d-flex align-items-center gap-2">
              <span>{t("Page Size:")}</span>
              <Form.Select
                size="sm"
                value={pageSize}
                disabled={isLoading}
                onChange={(e) => table.setPageSize(Number(e.target.value))}
                className="aa-table-select w-auto"
              >
                {pageSizeOptions.map((size) => (
                  <option key={size} value={size}>
                    {size}
                  </option>
                ))}
                {!serverPagination && <option value={1000000}>{t("Show All")}</option>}
              </Form.Select>
            </div>
            {serverPagination && (
              <span className="aa-table-total">
                {serverPagination.totalText ??
                  t("Total: {{total}}", { total: serverPagination.total.toLocaleString() })}
              </span>
            )}
          </div>

          <BasePages
            table={table}
            isFetching={isFetching}
            fileName={fileName}
            showPageNumber={true}
            showExport={!serverPagination}
          />
        </div>
        {/* Pagination Buttons */}
        {pageCount > 1 && (
          <div className="d-flex align-items-center gap-2">
            <Button
              size="sm"
              disabled={isLoading || !table.getCanPreviousPage()}
              onClick={() => table.setPageIndex(0)}
              className="aa-table-page-button"
              title={t("First Page")}
            >
              <ChevronFirst className="aa-table-page-icon" />
            </Button>
            <Button
              size="sm"
              disabled={isLoading || !table.getCanPreviousPage()}
              onClick={() => table.previousPage()}
              className="aa-table-page-button"
              title={t("Previous Page")}
            >
              <ChevronLeft className="aa-table-page-icon" />
            </Button>

            <span className="aa-table-page-number px-2 fw-bold">
              {t("Page {{page}} of {{total}}", {
                page: pageIndex + 1,
                total: pageCount,
              })}
            </span>

            <Button
              size="sm"
              disabled={isLoading || !table.getCanNextPage()}
              onClick={() => table.nextPage()}
              className="aa-table-page-button"
              title={t("Next Page")}
            >
              <ChevronRight className="aa-table-page-icon" />
            </Button>
            <Button
              size="sm"
              disabled={isLoading || !table.getCanNextPage()}
              onClick={() => table.setPageIndex(pageCount - 1)}
              className="aa-table-page-button"
              title={t("Last Page")}
            >
              <ChevronLast className="aa-table-page-icon" />
            </Button>
          </div>
        )}
        {footer && <div className="w-100">{footer}</div>}
      </div>

      {debugTable && (
        <div className="p-3">
          <div>{t("{{count}} Rows", { count: table.getRowModel().rows.length })}</div>
          <pre>{JSON.stringify(table.state, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default BaseTable;
