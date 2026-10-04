// React
import { useState } from "react";

// Third Party
import type { ColumnDef } from "@tanstack/react-table";
import { LoaderCircle } from "lucide-react";

import { LiveStatusIndicator, SecurityBadge } from "@/Components/Badges";
import { BaseTable } from "@/Components/Utils/BaseTable";
import {
  allianceImageUrl,
  characterImageUrl,
  corporationImageUrl,
  formatEveTime,
  formatNumber,
  formatRelativeTime,
  itemImageUrl,
  renderTooltip,
  shipImageUrl,
  toolTipContainer,
} from "@/Utils";

interface ShowcaseRow {
  pilot: string;
  hull: string;
  system: string;
  security: number;
  bounty: number;
}

const sampleRows: ShowcaseRow[] = [
  { pilot: "Aster Voss", hull: "Rifter", system: "Jita", security: 0.9, bounty: 1250000 },
  { pilot: "Mira Sato", hull: "Caracal", system: "Tama", security: 0.3, bounty: 48000000 },
  { pilot: "Kade Orlan", hull: "Vexor", system: "Hed", security: -0.2, bounty: 7600000 },
  { pilot: "Nia Corvus", hull: "Osprey", system: "Amarr", security: 1.0, bounty: 930000 },
  { pilot: "Tarin Hale", hull: "Merlin", system: "Rancer", security: 0.4, bounty: 1250000000 },
  { pilot: "Eris Vale", hull: "Thrasher", system: "Dodixie", security: 0.8, bounty: 31600000 },
];

const sampleTimestamp = new Date("2026-10-03T12:33:56Z").getTime();

const columns: ColumnDef<ShowcaseRow>[] = [
  { accessorKey: "pilot", header: "Pilot" },
  { accessorKey: "hull", header: "Ship" },
  { accessorKey: "system", header: "System" },
  {
    accessorKey: "security",
    header: "Security",
    cell: ({ getValue }) => <SecurityBadge sec={getValue<number>()} />,
  },
  {
    accessorKey: "bounty",
    header: "Bounty",
    cell: ({ getValue }) => formatNumber(getValue<number>()),
  },
];

const imageSamples = [
  { label: "Ship", source: shipImageUrl(587, 64), alt: "Rifter ship render" },
  { label: "Character", source: characterImageUrl(2112625428, 64), alt: "Character portrait" },
  { label: "Corporation", source: corporationImageUrl(1000125, 64), alt: "Corporation logo" },
  { label: "Alliance", source: allianceImageUrl(99000001, 64), alt: "Alliance logo" },
  { label: "Item", source: itemImageUrl(34, 64), alt: "Tritanium icon" },
];

function StyleGuide() {
  const [activeTab, setActiveTab] = useState("Overview");

  return (
    <main className="d-flex flex-column gap-4">
      <header>
        <h1 className="aa-section-title mb-1">AllianceAuth Style Test</h1>
        <p className="aa-section-subtitle mb-0">
          Shared CSS utilities, EVE helpers, and table variants.
        </p>
      </header>

      <section aria-labelledby="showcase-badges-heading">
        <h2 id="showcase-badges-heading" className="aa-section-title mb-3">
          Badges and status
        </h2>
        <div className="row g-3">
          <div className="col-lg-6">
            <article className="aa-panel h-100">
              <h3 className="aa-section-subtitle mb-3">Security badges</h3>
              <div className="d-flex flex-wrap align-items-center gap-2">
                <SecurityBadge sec={0.8} />
                <SecurityBadge sec={0.3} />
                <SecurityBadge sec={-0.2} />
                <span className="aa-badge aa-badge-hisec">AA Badge</span>
                <span className="aa-badge-xs aa-badge-lowsec">Compact</span>
              </div>
            </article>
          </div>
          <div className="col-lg-6">
            <article className="aa-panel h-100">
              <h3 className="aa-section-subtitle mb-3">Live status states</h3>
              <div className="d-flex flex-wrap align-items-center gap-4">
                <LiveStatusIndicator dataUpdatedAt={sampleTimestamp} showTimestamp />
                <LiveStatusIndicator isFetching showTimestamp />
                <LiveStatusIndicator isError showTimestamp />
              </div>
            </article>
          </div>
        </div>
      </section>

      <section aria-labelledby="showcase-panels-heading">
        <h2 id="showcase-panels-heading" className="aa-section-title mb-3">
          Panels and interaction utilities
        </h2>
        <div className="row g-3">
          <div className="col-lg-6">
            <article className="aa-panel h-100">
              <h3 className="aa-section-subtitle mb-2">Standard panel</h3>
              <p className="mb-0">The current page is inside the shared <code>aa-section</code> layout.</p>
            </article>
          </div>
          <div className="col-lg-6">
            <article className="aa-panel-lg h-100">
              <h3 className="aa-section-subtitle mb-2">Large panel</h3>
              <p className="mb-0">This panel uses the responsive large padding variant.</p>
            </article>
          </div>
          <div className="col-lg-6">
            <div className="aa-loader-container">
              <LoaderCircle className="me-2" size={18} aria-hidden="true" />
              <span>Loader container preview</span>
            </div>
          </div>
          <div className="col-lg-6">
            <div className="aa-panel h-100 d-flex flex-column justify-content-center gap-3">
              <div className="aa-border border rounded p-3">
                Border hover utility
              </div>
              <button className="aa-cursor-pointer btn btn-sm btn-outline-light" type="button">
                Pointer utility
              </button>
            </div>
          </div>
          <div className="col-lg-6">
            <div className="aa-tab-bar" role="tablist" aria-label="Preview tabs">
              {["Overview", "Activity", "Members"].map((tab) => (
                <button
                  key={tab}
                  type="button"
                  role="tab"
                  aria-selected={activeTab === tab}
                  className={`aa-tab-btn ${activeTab === tab ? "active" : ""}`}
                  onClick={() => setActiveTab(tab)}
                >
                  {tab}
                </button>
              ))}
            </div>
            <p className="aa-section-subtitle mt-2 mb-0">Selected: {activeTab}</p>
          </div>
          <div className="col-lg-6">
            <div className="aa-panel h-100 d-flex flex-wrap align-items-center gap-3">
              <div className="aa-portrait">
                <img src={characterImageUrl(2112625428, 64)} alt="Character portrait preview" />
              </div>
              <a
                className="aa-link p-2"
                href="https://zkillboard.com/"
                target="_blank"
                rel="noreferrer"
                style={{ backgroundColor: "var(--aa-color-white)" }}
              >
                AllianceAuth link
              </a>
              {renderTooltip(
                "Tooltip utility preview",
                <button className="btn btn-sm btn-outline-light" type="button">Tooltip</button>,
              )}
              {toolTipContainer("Static tooltip content")}
            </div>
          </div>
        </div>
      </section>

      <section aria-labelledby="showcase-helpers-heading">
        <h2 id="showcase-helpers-heading" className="aa-section-title mb-3">
          EVE helper previews
        </h2>
        <div className="aa-panel">
          <div className="d-flex flex-wrap align-items-center gap-4 mb-3">
            {imageSamples.map((image) => (
              <figure className="d-flex flex-column align-items-center gap-2 mb-0" key={image.label}>
                <img src={image.source} alt={image.alt} width={48} height={48} />
                <figcaption className="aa-section-subtitle">{image.label}</figcaption>
              </figure>
            ))}
          </div>
          <div className="d-flex flex-wrap gap-4">
            <span>{formatNumber(1250000000)}</span>
            <span>{formatEveTime(new Date("2026-10-03T12:34:56Z"))}</span>
            <span>{formatRelativeTime(new Date("2026-10-03T11:34:56Z"))}</span>
          </div>
        </div>
      </section>

      <section aria-labelledby="showcase-tables-heading">
        <h2 id="showcase-tables-heading" className="aa-section-title mb-1">
          Tables
        </h2>
        <p className="aa-section-subtitle mb-3">
          Both previews use local rows; headers sort and the controls paginate.
        </p>
        <div className="mb-4">
          <h3 className="aa-section-subtitle">AllianceAuth table</h3>
          <BaseTable
            columns={columns}
            data={sampleRows}
            initialState={{ pagination: { pageSize: 3 } }}
            pageSizeOptions={[3, 6]}
            itemLabel="pilots"
          />
        </div>
        <div>
          <h3 className="aa-section-subtitle">Bootstrap table</h3>
          <BaseTable
            variant="bootstrap"
            columns={columns}
            data={sampleRows}
            striped
            hover
            initialState={{ pagination: { pageSize: 3 } }}
            pageSizeOptions={[3, 6]}
            itemLabel="pilots"
          />
        </div>
      </section>
    </main>
  );
}

export default StyleGuide;