// src/components/auth/Register.jsx
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

export default function Register() {
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const basicServices = [
    { title: "Sign up" },
    { title: "Sign up" },
    { title: "Sign up" },
    { title: "Sign up" },
  ];

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      alert("Oops! Passwords do not match, please check again!");
      return;
    }
    console.log("Đang thử đăng ký với:", formData);
    // Thêm logic gọi API đăng ký của bạn ở đây
  };

  return (
    <div
      className="relative flex flex-col items-center justify-center w-full min-h-screen font-sans gap-12"
      style={{
        backgroundColor: "#FFFFFF",
        paddingTop: "40px",
        paddingBottom: "40px",
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
          width: "368px",
        }}
      >
        <CardHeader style={{ fontspacing: "0.02em" }}>
          <CardTitle
            style={{ fontSize: "1.0rem", color: "#191A23", fontWeight: "bold" }}
          >
            Create an account
          </CardTitle>
          <CardDescription
            style={{
              fontSize: "0.9rem",
              color: "#191A23",
              fontspacing: "0.02em",
            }}
          >
            Enter your details below to create an account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form
            id="register-form"
            onSubmit={handleRegister}
            className="flex flex-col gap-6"
          >
            {/* --- FULL NAME --- */}
            <div className="grid gap-2">
              <Label
                htmlFor="fullName"
                style={{
                  fontSize: "1.0rem",
                  color: "#191A23",
                  fontWeight: "bold",
                }}
              >
                Full Name
              </Label>
              <Input
                id="fullName"
                name="fullName"
                type="text"
                placeholder="What should we call you?"
                required
                value={formData.fullName}
                onChange={handleChange}
                className="focus-visible:ring-1 focus-visible:ring-[#191A23] focus-visible:ring-offset-0"
                style={{
                  border: "1px solid #191A23",
                  borderRadius: "5px",
                  backgroundColor: "#FFFFFF",
                  color: "#191A23",
                  fontSize: "1rem",
                  padding: "12px 8px",
                  marginTop: "8px",
                  marginBottom: "8px",
                }}
              />
            </div>

            {/* --- EMAIL --- */}
            <div className="grid gap-2">
              <Label
                htmlFor="email"
                style={{
                  fontSize: "1.0rem",
                  color: "#191A23",
                  fontWeight: "bold",
                }}
              >
                Email
              </Label>
              <Input
                id="email"
                name="email"
                type="email"
                placeholder="Tell us your email..."
                required
                value={formData.email}
                onChange={handleChange}
                className="focus-visible:ring-1 focus-visible:ring-[#191A23] focus-visible:ring-offset-0"
                style={{
                  border: "1px solid #191A23",
                  borderRadius: "5px",
                  backgroundColor: "#FFFFFF",
                  color: "#191A23",
                  fontSize: "1rem",
                  padding: "12px 8px",
                  marginTop: "8px",
                  marginBottom: "8px",
                }}
              />
            </div>

            {/* --- PASSWORD --- */}
            <div className="grid gap-2">
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
              <Input
                id="password"
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={handleChange}
                className="focus-visible:ring-1 focus-visible:ring-[#191A23] focus-visible:ring-offset-0"
                placeholder="Create a password..."
                style={{
                  border: "1px solid #191A23",
                  borderRadius: "5px",
                  backgroundColor: "#FFFFFF",
                  color: "#191A23",
                  fontSize: "1rem",
                  padding: "12px 8px",
                  marginTop: "8px",
                  marginBottom: "8px",
                }}
              />
            </div>

            {/* --- CONFIRM PASSWORD --- */}
            <div className="grid gap-2">
              <Label
                htmlFor="confirmPassword"
                style={{
                  fontSize: "1rem",
                  color: "#191A23",
                  fontWeight: "bold",
                }}
              >
                Confirm Password
              </Label>
              <Input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                required
                value={formData.confirmPassword}
                onChange={handleChange}
                className="focus-visible:ring-1 focus-visible:ring-[#191A23] focus-visible:ring-offset-0"
                placeholder="Repeat your password..."
                style={{
                  border: "1px solid #191A23",
                  borderRadius: "5px",
                  backgroundColor: "#FFFFFF",
                  color: "#191A23",
                  fontSize: "1rem",
                  padding: "12px 8px",
                  marginTop: "8px",
                  marginBottom: "8px",
                }}
              />
            </div>
          </form>
        </CardContent>

        {/* --- BUTTON --- */}
        <div className="flex flex-col gap-4 w-full">
          <button
            type="submit"
            form="register-form"
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
            Sign up
          </button>

          <div
            className="mt-4 text-center"
            style={{ fontSize: "1rem", color: "#191A23" }}
          >
            Already have an account?{" "}
            <Link
              to="/login"
              style={{
                textDecoration: "underline",
                textDecorationThickness: "1px",
                underlineOffset: "4px",
                fontWeight: "semibold",
                color: "#191A23",
              }}
              className="hover:opacity-80 transition-opacity"
            >
              Log in
            </Link>
          </div>
        </div>
      </Card>

      <div
        className="absolute flex flex-row flex-wrap justify-between gap-8 w-full"
        style={{ bottom: "40px", paddingLeft: "100px", paddingRight: "100px" }} // Tui nhớ thêm padding 100px cho má nha
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