export interface ErrorLoaderProps {
  message?: string;
  title?: string;
  /** Extra classes for the wrapper. */
  className?: string;
  /** Extra classes for the warning icon. */
  iconClassName?: string;
}

/** Centered warning icon with an optional title and message, e.g. for 404 and error pages. */
export const ErrorLoader = ({ message, title, className = "", iconClassName = "" }: ErrorLoaderProps = {}) => {
  return (
    <div className={`d-flex flex-column align-items-center justify-content-center ${className}`}>
      <span className="aa-shake d-inline-block">
        <i className={`fas fa-exclamation-triangle text-danger display-1 ${iconClassName}`}></i>
      </span>
      {title && <h3>{title}</h3>}
      {message && <p>{message}</p>}
    </div>
  );
};

export default ErrorLoader;
