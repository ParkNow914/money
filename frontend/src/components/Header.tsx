import { Link, NavLink } from "react-router-dom";

const navItems = [
  { to: "/", label: "Home" },
  { to: "/ia-demo", label: "IA Demo" },
  { to: "/marketplace", label: "Marketplace" },
  { to: "/admin", label: "Admin" },
];

function Header() {
  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="font-bold text-xl text-blue-600">
          Always Free AI
        </Link>
        <nav className="flex gap-4">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `text-sm font-semibold ${isActive ? "text-blue-600" : "text-slate-500"}`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  );
}

export default Header;
