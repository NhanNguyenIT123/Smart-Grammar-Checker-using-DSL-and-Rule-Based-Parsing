import { Link } from "react-router-dom";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { ChevronDown, History, Home, LogOut, Sparkles, User } from "lucide-react";

export default function WorkspaceNavbar({ currentUser, onLogout }) {
  return (
    <nav
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "0px 100px 0px 100px", 
        backgroundColor: "#B9FF66",
        height: "50px",
        boxShadow: "inset 0 0 0 2px black, 0 4px 4px rgba(0, 0, 0, 0.25)",
      }}
    >
      <Link to="/" style={{ textDecoration: "none" }}>
        <div
          style={{
            fontSize: "1rem",
            fontWeight: "600",
            color: "#000000",
            border: "2px solid black",
            backgroundColor: "#FFFFFF",
            boxShadow: "inset 0 0 0 2px white, 0 4px 4px rgba(0, 0, 0, 0.25)",
            padding: "2px 8px",
          }}
        >
          Grammar Checker
        </div>
      </Link>

      <div style={{ display: "flex", gap: "40px", alignItems: "center" }}>
        <Link
          to="/"
          style={{
            fontSize: "1rem",
            color: "#000000",
            textDecoration: "none",
            fontWeight: "200", 
          }}
          onMouseEnter={(e) => (e.target.style.textDecoration = "underline")}
          onMouseLeave={(e) => (e.target.style.textDecoration = "none")}
        >
          Getting started
        </Link>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <div
              className="outline-none border-none ring-0 focus:outline-none focus:ring-0 focus-visible:outline-none focus-visible:ring-0 data-[state=open]:!bg-transparent data-[state=open]:!outline-none bg-transparent"
              style={{
                appearance: "none", 
                WebkitAppearance: "none",
                color: "#000000",
                fontSize: "1rem",
                fontWeight: "200",
                cursor: "pointer",
                display: "flex",
                gap: "8px",
                alignItems: "center",
                border: "0px solid transparent",
                boxShadow: "none",
                padding: "8px 16px",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = "#000000";
                e.currentTarget.style.color = "#FFFFFF";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = "transparent";
                e.currentTarget.style.color = "#000000";
              }}
            >
              {currentUser?.displayName || "Account"} <ChevronDown size={20} strokeWidth={1.5} />
            </div>
          </DropdownMenuTrigger>

          <DropdownMenuContent
            align="end"
            style={{
              backgroundColor: "#FFFFFF",
              border: "1px solid #000000",
              borderRadius: "14px",
              boxShadow: "0 4px 12px rgba(0, 0, 0, 0.1)",
              padding: "10px",
              minWidth: "180px",
              marginTop: "8px",
            }}
          >
            <DropdownMenuItem 
                className="cursor-pointer focus:bg-gray-100 rounded-lg"
                style={{ padding: "12px", fontWeight: "200", fontSize: "1.1rem" }}
            >
              <div className="flex items-center gap-3">
                <User size={18} /> Profile
              </div>
            </DropdownMenuItem>

            <DropdownMenuItem 
                className="cursor-pointer focus:bg-gray-100 rounded-lg"
                style={{ padding: "12px", fontWeight: "200", fontSize: "1.1rem" }}
            >
              <div className="flex items-center gap-3">
                <History size={18} /> History
              </div>
            </DropdownMenuItem>

            <div style={{ height: "1px", backgroundColor: "#eee", margin: "8px 0" }} />

            <DropdownMenuItem className="p-0 focus:bg-transparent" onClick={onLogout}>
              <div
                style={{
                  width: "100%",
                  backgroundColor: "#B9FF66",
                  color: "#000000",
                  padding: "12px",
                  borderRadius: "10px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: "10px",
                  fontWeight: "600",
                  fontSize: "1.1rem",
                  cursor: "pointer",
                  transition: "all 0.2s",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = "#000000";
                  e.currentTarget.style.color = "#FFFFFF";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = "#B9FF66";
                  e.currentTarget.style.color = "#000000";
                }}
              >
                <LogOut size={18} /> Logout
              </div>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </nav>
  );
}
