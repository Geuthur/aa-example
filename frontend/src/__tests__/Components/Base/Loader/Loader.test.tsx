// Third Party
import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

// AA Example
import { ErrorBoundary, ErrorLoader, FetchingLoader } from "@/Components/Base/Loader";

describe("FetchingLoader", () => {
  it("should render a spinner with the message", () => {
    // Test Action
    const { container } = render(<FetchingLoader message="Loading pilots..." className="my-5" />);

    // Expected Result
    expect(screen.getByRole("status")).toHaveClass("spinner-border");
    expect(screen.getByText("Loading pilots...")).toBeInTheDocument();
    expect(container.firstElementChild).toHaveClass("d-flex", "my-5");
  });

  it("should add the spinner classes", () => {
    // Test Action
    render(<FetchingLoader spinnerClassName="spinner-border-sm" />);

    // Expected Result
    expect(screen.getByRole("status")).toHaveClass("spinner-border", "spinner-border-sm");
  });
});

describe("ErrorLoader", () => {
  it("should render the warning icon with title and message", () => {
    // Test Action
    const { container } = render(
      <ErrorLoader title="Error 404" message="Not found" className="mt-3" iconClassName="icon-x" />,
    );

    // Expected Result
    expect(screen.getByRole("heading", { level: 3 })).toHaveTextContent("Error 404");
    expect(screen.getByText("Not found")).toBeInTheDocument();
    expect(container.querySelector(".fa-exclamation-triangle")).toHaveClass("text-danger", "icon-x");
    expect(container.querySelector(".aa-shake")).toBeInTheDocument();
    expect(container.firstElementChild).toHaveClass("d-flex", "mt-3");
  });

  it("should render without title and message", () => {
    // Test Action
    render(<ErrorLoader />);

    // Expected Result
    expect(screen.queryByRole("heading")).not.toBeInTheDocument();
  });
});

describe("ErrorBoundary", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("should render the children while nothing fails", () => {
    // Test Action
    render(
      <ErrorBoundary>
        <p>All good</p>
      </ErrorBoundary>,
    );

    // Expected Result
    expect(screen.getByText("All good")).toBeInTheDocument();
  });

  it("should show the error and the component stack when a child throws", () => {
    // Test Data
    vi.spyOn(console, "error").mockImplementation(() => {});
    const Broken = () => {
      throw new Error("Boom");
    };

    // Test Action
    render(
      <ErrorBoundary traceClassName="trace-x">
        <Broken />
      </ErrorBoundary>,
    );

    // Expected Result
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Something went wrong.");
    expect(screen.getByRole("heading", { level: 3 })).toHaveTextContent("Error");
    expect(screen.getByText("Boom")).toBeInTheDocument();
    expect(screen.getByTestId("error-boundary-trace")).toHaveClass("border", "trace-x");
  });
});
