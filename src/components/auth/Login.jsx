// src/components/auth/Login.jsx
import { useState } from "react";
import { Link } from "react-router-dom";
import authbg from "@/assets/auth/authbg.svg";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const basicServices = [
    { title: "Log in" },
    { title: "Log in" },
    { title: "Log in" },
    { title: "Log in" },
  ];

  const handleLogin = (e) => {
    e.preventDefault();
    console.log("Đang thử đăng nhập với:", { email, password });
    // Thêm logic gọi API đăng nhập của bạn ở đây
  };

  return (
    <div
      className="relative flex flex-col items-center justify-center w-full min-h-screen font-sans gap-12"
      style={{ backgroundColor: "#FFFFFF", paddingTop: "40px", paddingBottom: "40px",
        backgroundImage: `url(${authbg})`, 
        backgroundSize: "auto",     
        backgroundPosition: "center", 
        backgroundRepeat: "no-repeat", 
       }}
    >
      <Card
        className="w-full max-w-sm"
        style={{
          backgroundColor: "#B9FF66",
          border: "2px solid #191A23",
          borderRadius: "5px",
          boxShadow: "4px 4px 0px 0px #191A23",
          padding: "24px",
          display: "flex",
          flexDirection: "column",
          gap: "24px",
          minHeight: "428px",
          width: "368px",
        }}
      >
        <CardHeader style={{ fontspacing: "0.02em" }}>
          <CardTitle
            style={{ fontSize: "1.0rem", color: "#191A23", fontWeight: "bold" }}
          >
            Login to your account
          </CardTitle>
          <CardDescription
            style={{
              fontSize: "0.9rem",
              color: "#191A23",
              fontspacing: "0.02em",
            }}
          >
            Enter your email below to login to your account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form
            id="login-form"
            onSubmit={handleLogin}
            className="flex flex-col gap-8"
            style={{}}
          >
            <div className="grid gap-2">
              <Label
                htmlFor="email"
                style={{
                  fontSize: "1.0rem",
                  color: "#191A23",
                  fontWeight: "bold",
                }}
              >
                Username
              </Label>
              <Input
                id="email"
                type="text"
                placeholder="Tell us your name..."
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="focus-visible:ring-1 focus-visible:ring-[#191A23] focus-visible:ring-offset-0"
                style={{
                  border: "1px solid #191A23",
                  borderRadius: "5px",
                  backgroundColor: "#FFFFFF",
                  color: "#191A23",
                  fontSize: "1rem",
                  padding: "12px 8px",
                  marginTop: "8px",
                  marginBottom: "16px",
                }}
              />
            </div>
            <div className="grid gap-2">
              <div className="flex items-center justify-between">
                <Label
                  htmlFor="password"
                  style={{
                    fontSize: "1rem",
                    color: "#191A23",
                    fontWeight: "bold",
                  }}
                >
                  Password
                </Label>
                <Link
                  to="/forgot-password"
                  style={{
                    fontSize: "1rem",
                    color: "#191A23",
                    textDecoration: "underline",
                    textDecorationThickness: "1px",
                    underlineOffset: "4px",
                    fontWeight: "semi-bold",
                    marginLeft: "auto",
                  }}
                  className="hover:opacity-80 transition-opacity"
                >
                  Forgot your password?
                </Link>
              </div>
              <Input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="focus-visible:ring-1 focus-visible:ring-[#191A23] focus-visible:ring-offset-0"
                placeholder="What's the password?..."
                style={{
                  border: "1px solid #191A23",
                  borderRadius: "5px",
                  backgroundColor: "#FFFFFF",
                  color: "#191A23",
                  fontSize: "1rem",
                  padding: "12px 8px",
                  marginTop: "8px",
                  marginBottom: "16px",
                }}
              />
            </div>
          </form>
        </CardContent>
        <div className="flex flex-col gap-4 w-full">
          <button
            type="submit"
            form="login-form"
            className="w-full bg-[#191A23] text-[#FFFFFF] hover:bg-[#F3F3F3] hover:text-[#191A23] transition-colors duration-200"
            style={{
              fontWeight: "bold",
              fontSize: "1rem",
              padding: "12px 0",
              borderRadius: "5px",
              cursor: "pointer",
              textTransform: "none",
              boxShadow: "0px 6px 0px 0px #191A23",
              border: "3px solid #191A23",
              marginBottom: "16px",
              outline: "none",
            }}
          >
            Login
          </button>

          <div
            className="mt-8 text-center"
            style={{ fontSize: "1rem", color: "#191A23" }}
          >
            Don&apos;t have an account?{" "}
            <Link
              to="/register"
              style={{
                textDecoration: "underline",
                textDecorationThickness: "1px",
                underlineOffset: "4px",
                fontWeight: "semibold",
                color: "#191A23",
              }}
              className="hover:opacity-80 transition-opacity"
            >
              Sign up
            </Link>
          </div>
        </div>
      </Card>

      <div 
        className="absolute flex flex-row flex-wrap justify-between gap-8 w-full"
        style={{ bottom: "40px" }}
      >
        {basicServices.map((service, index) => (
          <div
            key={index}
            className="flex-1 text-center"
            style={{ color: "#191A23" }}
          >
            <h3 className="text-xl font-bold">{service.title}</h3>
          </div>
        ))}
      </div>

    </div>
  );
}