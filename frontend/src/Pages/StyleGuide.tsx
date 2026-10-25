// React
import { useState } from "react";

// Third Party
import type { ColumnDef } from "@tanstack/react-table";
import { Badge, Button, Card } from "react-bootstrap";

import { BaseModal, ModalSize } from "@/Components/Base/BaseModal";
import { BaseTable } from "@/Components/Base/BaseTable";
import {
  allianceImageUrl,
  characterImageUrl,
  corporationImageUrl,
  formatCompactNumber,
  formatEveTime,
  formatIsk,
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

const securityVariant = (sec: number) => (sec >= 0.5 ? "success" : sec > 0 ? "warning" : "danger");

const columns: ColumnDef<ShowcaseRow>[] = [
  { accessorKey: "pilot", header: "Pilot" },
  { accessorKey: "hull", header: "Ship" },
  { accessorKey: "system", header: "System" },
  {
    accessorKey: "security",
    header: "Security",
    cell: ({ getValue }) => (
      <Badge bg={securityVariant(getValue<number>())}>{getValue<number>().toFixed(1)}</Badge>
    ),
  },
  {
    accessorKey: "bounty",
    header: "Bounty",
    meta: { align: "right" },
    cell: ({ getValue }) => <span className="text-end d-block">{formatIsk(getValue<number>())}</span>,
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
  const [showModalTable, setShowModalTable] = useState(false);
  const [showConfirmModal, setShowConfirmModal] = useState(false);

  return (
    <div className="d-flex flex-column gap-4">
      <header>
        <h1 className="h3 mb-1">AllianceAuth Style Test</h1>
        <p className="text-secondary mb-0">Bootstrap building blocks, EVE helpers, and table variants.</p>
      </header>

      <section aria-labelledby="showcase-badges-heading">
        <h2 id="showcase-badges-heading" className="h5 mb-3">
          Badges and buttons
        </h2>
        <Card className="bg-dark border-secondary">
          <Card.Body className="d-flex flex-wrap align-items-center gap-2">
            <Badge bg="success">Highsec</Badge>
            <Badge bg="warning">Lowsec</Badge>
            <Badge bg="danger">Nullsec</Badge>
            <Badge bg="primary">Primary</Badge>
            <Badge bg="info">Info</Badge>
            <Button size="sm" variant="primary">Primary</Button>
            <Button size="sm" variant="secondary">Secondary</Button>
            <Button size="sm" variant="success">Success</Button>
            <Button size="sm" variant="warning">Warning</Button>
            <Button size="sm" variant="danger">Danger</Button>
          </Card.Body>
        </Card>
      </section>

      <section aria-labelledby="showcase-interaction-heading">
        <h2 id="showcase-interaction-heading" className="h5 mb-3">
          Tooltips and links
        </h2>
        <Card className="bg-dark border-secondary">
          <Card.Body className="d-flex flex-wrap align-items-center gap-3">
            <a href="https://zkillboard.com/" target="_blank" rel="noreferrer">
              AllianceAuth link
            </a>
            {renderTooltip(
              "Tooltip utility preview",
              <button className="btn btn-sm btn-outline-light" type="button">Tooltip</button>,
            )}
            {toolTipContainer("Static tooltip content")}
          </Card.Body>
        </Card>
      </section>

      <section aria-labelledby="showcase-helpers-heading">
        <h2 id="showcase-helpers-heading" className="h5 mb-3">
          EVE helper previews
        </h2>
        <Card className="bg-dark border-secondary">
          <Card.Body>
            <div className="d-flex flex-wrap align-items-center gap-4 mb-3">
              {imageSamples.map((image) => (
                <figure className="d-flex flex-column align-items-center gap-2 mb-0" key={image.label}>
                  <img src={image.source} alt={image.alt} width={48} height={48} />
                  <figcaption className="text-secondary small">{image.label}</figcaption>
                </figure>
              ))}
            </div>
            <div className="d-flex flex-wrap gap-4">
              <span>{formatCompactNumber(1250000000, "ISK")}</span>
              <span>{formatIsk(1234567.89)}</span>
              <span>{formatEveTime(new Date("2026-10-03T12:34:56Z"))}</span>
              <span>{formatRelativeTime(new Date("2026-10-03T11:34:56Z"))}</span>
            </div>
          </Card.Body>
        </Card>
      </section>

      <section aria-labelledby="showcase-tables-heading">
        <h2 id="showcase-tables-heading" className="h5 mb-1">
          Tables
        </h2>
        <p className="text-secondary mb-3">
          Both previews use local rows; headers sort and the controls paginate.
        </p>
        <div className="mb-4">
          <h3 className="h6">Default table</h3>
          <BaseTable
            columns={columns}
            data={sampleRows}
            initialState={{ pagination: { pageSize: 3 } }}
            pageSizeOptions={[3, 6]}
          />
        </div>
        <div>
          <div className="d-flex justify-content-between align-items-center mb-2">
            <div>
              <h3 className="h6 mb-0">Light table (cards and modals)</h3>
              <p className="text-secondary small mb-0">
                Use <code>variant=&quot;light&quot;</code> inside cards and modal bodies.
              </p>
            </div>
            <div className="d-flex gap-2">
              <Button variant="outline-info" size="sm" onClick={() => setShowModalTable(true)}>
                Preview in Modal
              </Button>
              <Button variant="outline-warning" size="sm" onClick={() => setShowConfirmModal(true)}>
                Preview Confirm Modal
              </Button>
            </div>
          </div>
          <Card className="bg-dark border-secondary">
            <Card.Body>
              <BaseTable
                variant="light"
                columns={columns}
                data={sampleRows}
                initialState={{ pagination: { pageSize: 3 } }}
                pageSizeOptions={[3, 6]}
              />
            </Card.Body>
          </Card>
        </div>
      </section>

      <BaseModal
        title="Modal Table Showcase"
        size={ModalSize.extraLarge}
        show={showModalTable}
        onHide={() => setShowModalTable(false)}
      >
        <h4 className="h6 mb-2">Roster in modal (light variant)</h4>
        <BaseTable
          variant="light"
          columns={columns}
          data={sampleRows}
          initialState={{ pagination: { pageSize: 3 } }}
          pageSizeOptions={[3, 6]}
        />
      </BaseModal>

      <BaseModal
        variant="confirm"
        data={{
          modal_id: "modal-confirm-showcase",
          title: "Confirm Modal Showcase",
          text: "Preview confirm modal",
          icon: "fas fa-check",
          buttonText: "Confirm",
          url: "#",
          color: "danger",
        }}
        size={ModalSize.medium}
        showModal={showConfirmModal}
        setShowModal={setShowConfirmModal}
        onApprove={async () => undefined}
      >
        <p className="mb-0">Are you sure you want to run this action?</p>
      </BaseModal>
    </div>
  );
}

export default StyleGuide;
