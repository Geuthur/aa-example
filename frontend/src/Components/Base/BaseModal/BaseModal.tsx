// React
import { useState } from "react";
import type { ReactNode } from "react";

// Third Party
import { Alert, Button, Modal } from "react-bootstrap";
import { useTranslation } from "react-i18next";

import { MODAL_DEFAULTS } from "@/Components/Base/BaseModal/BaseModalProps";
import type {
  BaseModalProps,
  BaseModalSharedProps,
  ConfirmModalProps,
  DefaultModalProps,
  ModalFormData,
} from "@/Components/Base/BaseModal/BaseModalProps";

interface ModalShellProps extends BaseModalSharedProps {
  show: boolean;
  onHide: () => void;
  onEnter?: () => void;
  title: ReactNode;
  footer: ReactNode | null;
  children?: ReactNode;
}

/** Gemeinsamer Rahmen (Header / Body / Footer) für alle Varianten. */
function ModalShell({
  show,
  onHide,
  onEnter,
  onShow,
  onExited,
  title,
  footer,
  children,
  size = MODAL_DEFAULTS.size,
  centered = MODAL_DEFAULTS.centered,
  scrollable = MODAL_DEFAULTS.scrollable,
  backdrop = MODAL_DEFAULTS.backdrop,
  restoreFocus = MODAL_DEFAULTS.restoreFocus,
  closeButton = MODAL_DEFAULTS.closeButton,
  className,
  bodyClassName,
  titleClassName,
}: ModalShellProps) {
  return (
    <Modal
      show={show}
      size={size}
      onHide={onHide}
      onEnter={onEnter}
      onShow={onShow}
      onExited={onExited}
      centered={centered}
      scrollable={scrollable}
      backdrop={backdrop}
      restoreFocus={restoreFocus}
      dialogClassName={className}
    >
      <Modal.Header closeButton={closeButton}>
        <Modal.Title className={titleClassName}>{title}</Modal.Title>
      </Modal.Header>
      <Modal.Body className={bodyClassName}>{children}</Modal.Body>
      {footer !== null && <Modal.Footer>{footer}</Modal.Footer>}
    </Modal>
  );
}

/** Normales Modal: zeigt nur die übergebenen Children an. */
function DefaultModal({
  show,
  onHide,
  title,
  children,
  footer,
  hideFooter = false,
  closeText,
  closeVariant = MODAL_DEFAULTS.closeVariant,
  ...shared
}: DefaultModalProps) {
  const { t } = useTranslation();

  const defaultFooter = (
    <Button variant={closeVariant} onClick={onHide}>
      {closeText ?? t("Close")}
    </Button>
  );

  return (
    <ModalShell
      {...shared}
      show={show}
      onHide={onHide}
      title={title}
      footer={hideFooter ? null : (footer ?? defaultFooter)}
    >
      {children}
    </ModalShell>
  );
}

/** Bestätigungs-Modal: verarbeitet Daten über `onApprove` (optional mit Formular). */
function ConfirmModal({
  data: ModalData,
  showModal,
  setShowModal,
  onApprove,
  isPending = false,
  validate,
  initialFormData,
  title,
  confirmText,
  confirmVariant,
  closeText,
  closeVariant = MODAL_DEFAULTS.closeVariant,
  children,
  ...shared
}: ConfirmModalProps) {
  const { t } = useTranslation();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [formData, setFormData] = useState<ModalFormData>(initialFormData ?? {});
  const [validated, setValidated] = useState(false);

  const resetState = () => {
    setErrorMessage(null);
    setFormData(initialFormData ?? {});
    setValidated(false);
  };
  const handleClose = () => {
    resetState();
    setShowModal(false);
  };
  const handleApprove = async () => {
    if (validate && !validate(formData)) {
      setValidated(true);
      return;
    }
    try {
      await onApprove({ url: ModalData.url, formData });
      // Erfolgreich:
      handleClose();
    } catch (error: unknown) {
      setErrorMessage(error instanceof Error ? error.message : 'An unexpected error occurred.');
    }
  };

  const renderedChildren =
    typeof children === 'function'
      ? children({ formData, onChange: setFormData })
      : children;

  const footer = (
    <>
      <Button
        variant={confirmVariant ?? ModalData.color ?? MODAL_DEFAULTS.confirmVariant}
        disabled={isPending}
        onClick={handleApprove}
      >
        {isPending ? t("Loading...") : confirmText || ModalData.buttonText || t("Confirm")}
      </Button>
      <Button variant={closeVariant} onClick={handleClose}>
        {closeText ?? t("Close")}
      </Button>
    </>
  );

  return (
    <ModalShell
      {...shared}
      show={showModal}
      onHide={handleClose}
      onEnter={resetState}
      title={title ?? ModalData.title}
      footer={footer}
    >
      {errorMessage && (
        <Alert variant="danger" onClose={() => setErrorMessage(null)} dismissible>
          {errorMessage}
        </Alert>
      )}
      <div className={validated ? 'was-validated' : ''}>
        {renderedChildren}
      </div>
    </ModalShell>
  );
}

/**
 * BaseModal mit zwei Varianten:
 * - `variant="default"` (Standard): normales Modal, Body = `children`, Footer = Schließen-Button.
 * - `variant="confirm"`: Bestätigungs-Modal mit `onApprove`, optional Formular via Render-Children.
 *
 * Alle Darstellungs-Werte (size, centered, backdrop, ...) sind optional und
 * fallen auf `MODAL_DEFAULTS` zurück.
 */
function BaseModal(props: BaseModalProps) {
  if (props.variant === "confirm") {
    return <ConfirmModal {...props} />;
  }
  return <DefaultModal {...props} />;
}

export default BaseModal;
