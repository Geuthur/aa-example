export interface FetchingLoaderProps {
  message?: string;
  /** Extra classes for the wrapper. */
  className?: string;
  /** Extra classes for the spinner, e.g. `spinner-border-sm`. */
  spinnerClassName?: string;
}

/** Centered Bootstrap spinner with an optional message. */
export const FetchingLoader = ({ message, className = "", spinnerClassName = "" }: FetchingLoaderProps = {}) => {
  return (
    <div className={`d-flex flex-column align-items-center justify-content-center ${className}`}>
      <div className={`spinner-border text-info ${spinnerClassName}`} role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      {message && (
        <span>
          {message}
        </span>
      )}
    </div>
  );
};

export default FetchingLoader;
