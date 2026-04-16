import { Button } from "@/components/ui/button";

export default function Navigation() {
  return (
    <nav
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "32px 48px",
        backgroundColor: "#F3F3F3",
      }}
    >
      <div
        style={{
          fontSize: "1.25 rem",
          fontWeight: "400",
          color: "#000000",
          border: "2px solid black",
          boxShadow: "inset 0 0 0 2px white, 0 4px 4px rgba(0, 0, 0, 0.25)",
        }}
      >
        Grammar Checker
      </div>

      <div
        style={{
          display: "flex",
          gap: "20px",
          alignItems: "center",
        }}
      >
        <div
          style={{
            display: "flex",
            gap: "20px",
            alignItems: "center",
          }}
        >
          <a
            href="#"
            style={{
              fontSize: "1 rem",
              color: "#000000",
              textDecoration: "none",
              fontWeight: "200",
            }}
            onMouseEnter={(e) => (e.target.style.textDecoration = "underline")}
            onMouseLeave={(e) => (e.target.style.textDecoration = "none")}
          >
            About us
          </a>
          <a
            href="#"
            style={{
              fontSize: "1 rem",
              color: "#000000",
              textDecoration: "none",
              fontWeight: "200",
            }}
            onMouseEnter={(e) => (e.target.style.textDecoration = "underline")}
            onMouseLeave={(e) => (e.target.style.textDecoration = "none")}
          >
            Services
          </a>
        </div>

        <div
          style={{
            display: "flex",
            gap: "16px",
            alignItems: "center",
          }}
        >
          <Button
            variant="outline"
            style={{
              border: "2px solid #000000",
              color: "#000000",
              padding: "8px 32px",
              fontSize: "1rem",
              borderRadius: "8px",
              fontWeight: "200",
              backgroundColor: "#F3F3F3",
              cursor: "pointer",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = "#000000";
              e.currentTarget.style.color = "#F3F3F3";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = "#F3F3F3";
              e.currentTarget.style.color = "#000000";
            }}
          >
            Login
          </Button>
          <Button
            variant="outline"
            style={{
              border: "2px solid #000000",
              color: "#000000",
              padding: "8px 32px",
              fontSize: "1rem",
              borderRadius: "8px",
              fontWeight: "200",
              backgroundColor: "#F3F3F3",
              cursor: "pointer",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = "#000000";
              e.currentTarget.style.color = "#F3F3F3";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = "#F3F3F3";
              e.currentTarget.style.color = "#000000";
            }}
          >
            Sign up
          </Button>
        </div>
      </div>
    </nav>
  );
}
