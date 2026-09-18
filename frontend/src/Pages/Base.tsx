
// React
import { Outlet } from "react-router";

// Third Party
import { Col } from "react-bootstrap";

import AuthMenuAsync from "@/Menu/AuthMenuAsync";
import { ErrorBoundary } from "@/Components/Loader";

const AuthBase = () => {
  return (
    <>
      <AuthMenuAsync />
      <Col>
        <div className="mt-4">
          <ErrorBoundary>
            <Outlet /> {/* Render the Children here */}
          </ErrorBoundary>
        </div>
      </Col>
    </>
  );
};

export default AuthBase;
