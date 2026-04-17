// src/components/auth/ForgotPassword.jsx
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

// Tạo sẵn một cái Icon mũi tên thuần bằng SVG thay cho MUI ArrowBackIcon
const ArrowLeftIcon = () => (
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    width="20" 
    height="20" 
    viewBox="0 0 24 24" 
    fill="none" 
    stroke="currentColor" 
    strokeWidth="2.5" 
    strokeLinecap="round" 
    strokeLinejoin="round"
  >
    <path d="m12 19-7-7 7-7"/>
    <path d="M19 12H5"/>
  </svg>
);

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [isSubmitted, setIsSubmitted] = useState(false);

  const basicServices = [
    { title: "Reset Password" },
    { title: "Reset Password" },
    { title: "Reset Password" },
    { title: "Reset Password" },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Đang gửi link reset password tới:", email);
    // Giả lập gọi API thành công
    setIsSubmitted(true);
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
            Reset Password
          </CardTitle>
          <CardDescription
            style={{
              fontSize: "0.9rem",
              color: "#191A23",
              fontspacing: "0.02em",
              lineHeight: "1.6",
            }}
          >
            {isSubmitted
              ? "We have sent a password reset link to your email. Please check your inbox."
              : "Enter your email address and we'll send you a link to reset your password."}
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          {/* NẾU CHƯA SUBMIT THÌ HIỆN FORM NHẬP EMAIL */}
          {!isSubmitted && (
            <form
              id="forgot-form"
              onSubmit={handleSubmit}
              className="flex flex-col gap-6"
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
                  Email
                </Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="Tell us your email..."
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
                    marginBottom: "8px",
                  }}
                />
              </div>
            </form>
          )}
        </CardContent>

        <div className="flex flex-col gap-4 w-full">
          {/* NÚT BẤM SẼ THAY ĐỔI DỰA THEO TRẠNG THÁI */}
          {!isSubmitted ? (
            <button
              type="submit"
              form="forgot-form"
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
              Send Reset Link
            </button>
          ) : (
            <button
              type="button"
              onClick={() => setIsSubmitted(false)}
              className="w-full bg-[#FFFFFF] text-[#191A23] hover:bg-[#191A23] hover:text-[#FFFFFF] transition-colors duration-200"
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
              Try another email
            </button>
          )}

          {/* QUAY LẠI TRANG LOGIN */}
          <div
            className="mt-4 flex justify-center items-center"
            style={{ fontSize: "1rem", color: "#191A23" }}
          >
            <Link
              to="/login"
              style={{
                textDecoration: "underline",
                textDecorationThickness: "1px",
                underlineOffset: "4px",
                fontWeight: "semibold",
                color: "#191A23",
                display: "flex",
                alignItems: "center",
                gap: "8px"
              }}
              className="hover:opacity-80 transition-opacity"
            >
              <ArrowLeftIcon /> Back to log in
            </Link>
          </div>
        </div>
      </Card>

      {/* --- 4 CHỮ RESET PASSWORD DƯỚI ĐÁY --- */}
      <div
        className="absolute flex flex-row flex-wrap justify-between gap-8 w-full"
        style={{ bottom: "40px", paddingLeft: "100px", paddingRight: "100px" }}
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