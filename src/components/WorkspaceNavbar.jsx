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
        padding: "0 2rem", 
        backgroundColor: "#B9FF66",
        height: "64px",
        boxShadow: "inset 0 0 0 2px black, 0 4px 4px rgba(0, 0, 0, 0.25)",
        position: "relative",
        zIndex: 50
      }}
    >
      <Link 
        to="/" 
        style={{ 
          textDecoration: "none", 
          display: "inline-block", 
          width: "max-content",
          flexShrink: 0
        }}
      >
        <div
          style={{
            fontSize: "1rem",
            fontWeight: "600",
            color: "#000000",
            border: "2px solid black",
            backgroundColor: "#FFFFFF",
            boxShadow: "inset 0 0 0 2px white, 0 4px 4px rgba(0, 0, 0, 0.25)",
            padding: "4px 12px",
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
            color: "#111827",
            textDecoration: "none",
            fontWeight: "700",
            letterSpacing: "0.01em",
          }}
          onMouseEnter={(e) => (e.target.style.textDecoration = "underline")}
          onMouseLeave={(e) => (e.target.style.textDecoration = "none")}
        >
          Getting started
        </Link>

        <DropdownMenu modal={false}>
          <DropdownMenuTrigger asChild>
            <div
              className="outline-none border-none ring-0 focus:outline-none focus:ring-0 focus-visible:outline-none focus-visible:ring-0 data-[state=open]:!bg-transparent data-[state=open]:!outline-none bg-transparent"
              style={{
                appearance: "none", 
                WebkitAppearance: "none",
                color: "#111827",
                fontSize: "1rem",
                fontWeight: "600",
                cursor: "pointer",
                display: "flex",
                gap: "8px",
                alignItems: "center",
                border: "2px solid #191A23",
                boxShadow: "2px 2px 0px 0px #191A23",
                borderRadius: "10px",
                backgroundColor: "#F8FFEE",
                padding: "6px 12px",
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
              <span style={{ display: "flex", flexDirection: "column", lineHeight: 1.1 }}>
                <span style={{ fontWeight: 700 }}>{currentUser?.displayName || "Account"}</span>
                <small
                  style={{
                    fontSize: "0.72rem",
                    opacity: 0.95,
                    textTransform: "capitalize",
                    backgroundColor: "rgba(25, 26, 35, 0.1)",
                    borderRadius: "999px",
                    padding: "2px 8px",
                    width: "fit-content",
                    marginTop: "4px",
                    fontWeight: 600,
                  }}
                >
                  {currentUser?.role || "guest"}
                </small>
              </span>
              <ChevronDown size={20} strokeWidth={1.5} />
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
