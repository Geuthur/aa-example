// React
import { useMemo } from "react";

// Third Party
import { BaseTable, createBaseColumnHelper, formatIsk, formatRelativeTime } from "aa-geuthur-react";
import { RefreshCw } from "lucide-react";
import { Button } from "react-bootstrap";
import { useTranslation } from "react-i18next";

// AA Example
import type { CharacterSchema } from "@/Api/schema";
import { CharacterStatusBadge } from "@/Components/Character/CharacterStatusBadge";

const columnHelper = createBaseColumnHelper<CharacterSchema>();

export interface CharacterTableProps {
  characters: CharacterSchema[];
  isLoading?: boolean;
  isFetching?: boolean;
  isError?: boolean;
  /** Called with the EVE character id when the update button of a row is clicked. */
  onUpdate: (characterId: number) => void;
  /** The character whose update is being queued; its button is disabled. */
  updatingCharacterId?: number;
}

/** Lists the characters with wallet balance, update status and an update button. */
export const CharacterTable = ({
  characters,
  isLoading = false,
  isFetching = false,
  isError = false,
  onUpdate,
  updatingCharacterId,
}: CharacterTableProps) => {
  const { t } = useTranslation();

  const columns = useMemo(
    () => [
      columnHelper.accessor("character_name", {
        header: t("Character"),
        cell: ({ row }) => (
          <div className="d-flex align-items-center gap-2">
            <img
              src={row.original.portrait_url}
              alt={row.original.character_name}
              className="rounded"
              width={32}
              height={32}
            />
            <span>{row.original.character_name}</span>
          </div>
        ),
      }),
      columnHelper.accessor("corporation_name", {
        header: t("Corporation"),
      }),
      columnHelper.accessor("wallet_balance", {
        header: t("Wallet"),
        meta: { align: "right" },
        enableColumnFilter: false,
        cell: ({ getValue }) => {
          const value = getValue();
          return value === null || value === undefined ? "-" : formatIsk(value);
        },
      }),
      columnHelper.accessor("update_status", {
        header: t("Status"),
        cell: ({ row }) => (
          <CharacterStatusBadge
            status={row.original.update_status}
            label={row.original.update_status_label}
          />
        ),
      }),
      columnHelper.accessor("last_update", {
        header: t("Last Update"),
        enableColumnFilter: false,
        cell: ({ getValue }) => formatRelativeTime(getValue()),
      }),
      columnHelper.display({
        id: "actions",
        header: t("Actions"),
        meta: { align: "right" },
        cell: ({ row }) => (
          <Button
            size="sm"
            variant="outline-light"
            title={t("Update")}
            aria-label={t("Update {{name}}", { name: row.original.character_name })}
            disabled={updatingCharacterId === row.original.character_id}
            onClick={() => onUpdate(row.original.character_id)}
          >
            <RefreshCw size={14} />
          </Button>
        ),
      }),
    ],
    [t, onUpdate, updatingCharacterId],
  );

  return (
    <BaseTable
      columns={columns}
      data={characters}
      isLoading={isLoading}
      isFetching={isFetching}
      isError={isError}
      loadingText={t("Loading characters...")}
      emptyText={t("No characters registered yet.")}
      exportFileName="characters.csv"
    />
  );
};

export default CharacterTable;
