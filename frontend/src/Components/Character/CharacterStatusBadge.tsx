// Third Party
import { Badge } from "react-bootstrap";

const STATUS_VARIANTS: Record<string, string> = {
  ok: "success",
  error: "danger",
  token_error: "warning",
  incomplete: "secondary",
  in_progress: "info",
  disabled: "dark",
};

export interface CharacterStatusBadgeProps {
  /** The `update_status` value of the API, e.g. `ok` or `token_error`. */
  status: string;
  /** The translated label shown in the badge. */
  label: string;
}

/** Shows the aggregate update status of a character as a Bootstrap badge. */
export const CharacterStatusBadge = ({ status, label }: CharacterStatusBadgeProps) => (
  <Badge bg={STATUS_VARIANTS[status] ?? "secondary"} data-testid="character-status-badge" data-status={status}>
    {label}
  </Badge>
);

export default CharacterStatusBadge;
