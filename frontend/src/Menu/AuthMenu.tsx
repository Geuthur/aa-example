import { MenuItem } from "@/Menu/BaseMenu";
import type { MenuLinkItem, MenuProps } from "@/Menu/BaseMenu";
import { ProjectName } from "@/App";

const AuthMenu = ({ data }: MenuProps) => {
  const toPath = (link: string) => `/${ProjectName}/${link}/`;

  const menuItems = Array.isArray(data)
    ? data.filter((item): item is MenuLinkItem => !!item.link)
    : [];

  return (
    <>
      {menuItems.map((item) => {
        return <MenuItem key={item.link} link={item} {...{ toPath }} />;
      })}
    </>
  );
};

export default AuthMenu;
