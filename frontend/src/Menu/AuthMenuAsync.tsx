// React
import ReactDOM from "react-dom";

// Third Party
import { useQuery } from "@tanstack/react-query";

import { loadMenu } from "@/Api/ApiCalls"
import { queryKeys } from "@/Api/query";
import AuthMenu from "@/Menu/AuthMenu";

const menuRoot = document.getElementById("nav-left");

const AuthMenuAsync = () => {
  const { isLoading, error, data } = useQuery({
    queryKey: queryKeys.Menu,
    queryFn: () => loadMenu(),
    refetchOnWindowFocus: false,
  });

  if (!menuRoot || !data?.links) {
    return <></>;
  }

  return ReactDOM.createPortal(
    <AuthMenu error={error ? true : false} isLoading={isLoading} data={data.links} />,
    menuRoot,
  );
};

export default AuthMenuAsync;
