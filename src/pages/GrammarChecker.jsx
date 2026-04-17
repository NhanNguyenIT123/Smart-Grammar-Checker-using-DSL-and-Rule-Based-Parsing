// src/pages/GrammarChecker.jsx
import React from "react";
import checkerbg from "../assets/mainpage/mainpagebg.svg";
import { Textarea } from "@/components/ui/textarea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import MainNavbar from "@/components/MainNavbar";

export default function GrammarChecker() {
  return (
    <>
      <div
        style={{
          position: "fixed",
          top: "0",
          left: "0",
          width: "100%",
          zIndex: "100",
        }}
      >
        <MainNavbar />
      </div>

      <div
        className="min-h-screen w-full font-sans flex justify-center p-8 px-12 relative"
        style={{
          backgroundRepeat: "no-repeat",
          paddingTop: "120px",
          overflow: "hidden",
        }}
      >
        {/* THẺ ẢNH NỀN ÉP CỨNG DƯỚI CÙNG */}
        <img
          src={checkerbg}
          alt="background"
          className="absolute  -z-10 pointer-events-none"
          style={{
            top: "-0",
            width: "100%",
            objectFit: "cover",
          }}
        />

        <div
          className="flex flex-row gap-12 w-full"
          style={{ maxWidth: "1400px", gap: "60px", margin: "0 auto" }}
        >
          <div
            className="flex flex-col"
            style={{
              width: "55%", // KHÓA CỨNG CHIỀU RỘNG
              backgroundColor: "#FFFFFF",
              border: "4px solid #191A23",
              borderRadius: "12px",
              boxShadow: "8px 8px 0px 0px #191A23",
              padding: "40px",
              height: "fit-content",
            }}
          >
            {/* Header của cột trái */}
            <div className="flex flex-row justify-between items-center mb-2">
              <h1
                style={{
                  fontSize: "2.5rem",
                  fontWeight: "bold",
                  color: "#191A23",
                  margin: 0,
                }}
              >
                DSL Input
              </h1>
              <button
                style={{
                  backgroundColor: "#B9FF66",
                  color: "#191A23",
                  fontWeight: "bold",
                  fontSize: "1rem",
                  padding: "10px 24px",
                  borderRadius: "8px",
                  border: "2px solid #191A23",
                  boxShadow: "3px 3px 0px 0px #191A23",
                  cursor: "pointer",
                  transition: "all 0.2s",
                }}
                className="hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[1px_1px_0px_0px_#191A23]"
              >
                Run Command
              </button>
            </div>

            <p
              style={{
                fontSize: "1.1rem",
                color: "#191A23",
                marginBottom: "24px",
              }}
            >
              input your text to check the grammar.
            </p>

            <Textarea
              placeholder="Type your message here."
              className="focus-visible:ring-0 focus-visible:ring-offset-0 resize-none"
              style={{
                flexGrow: 1,
                minHeight: "450px",
                border: "2px solid #191A23",
                borderRadius: "8px",
                fontSize: "1.1rem",
                padding: "16px",
                color: "#191A23",
              }}
            />
          </div>

          {/* =======================================================
            CỘT PHẢI: TABS & RESULTS (Ép cứng rộng 40%)
            ======================================================= */}
          <div
            className="flex flex-col"
            style={{ width: "35%" }} // KHÓA CỨNG CHIỀU RỘNG
          >
            <Tabs
              defaultValue="result"
              className="w-full"
              style={{
                height: "fit-content",
                display: "flex",
                flexDirection: "column",
                gap: "16px",
              }}
            >
              {/* THÀNH PHẦN TABS LIST - ĐÃ ÉP ĐỔI MÀU KHI CLICK */}

              <TabsList
                className="w-full flex p-0"
                style={{
                  backgroundColor: "#B9FF66",
                  border: "4px solid #191A23",
                  borderRadius: "10px",
                  boxShadow: "6px 6px 0px 0px #191A23",
                  height: "65px",
                  overflow: "hidden",
                }}
              >
                <TabsTrigger
                  value="result"
                  className="flex-1 h-full font-bold text-[1.1rem] rounded-none  p-4 shadow-none 
               transition-colors duration-200
               bg-[#B9FF66] text-[#191A23] hover:bg-[#A2E655]
               data-[active]:!bg-[#191A23] data-[active]:!text-[#FFFFFF]"
                >
                  Result
                </TabsTrigger>

                <TabsTrigger
                  value="help"
                  className="flex-1 h-full font-bold text-[1.1rem] rounded-none p-4 shadow-none 
               transition-colors duration-200
               /* Mặc định màu xanh */
               bg-[#B9FF66] text-[#191A23] hover:bg-[#A2E655]
               /* ÉP MÀU KHI ACTIVE BẰNG TIỀN TỐ ! quan trọng */
               data-[active]:!bg-[#191A23] data-[active]:!text-[#FFFFFF]"
                >
                  Help
                </TabsTrigger>
              </TabsList>
              {/* NỘI DUNG TAB: RESULT */}
              <TabsContent value="result" className="mt-8 m-0 p-0">
                <div
                  style={{
                    backgroundColor: "#B9FF66",
                    border: "4px solid #191A23",
                    borderRadius: "8px",
                    boxShadow: "6px 6px 0px 0px #191A23",
                    padding: "24px",
                    display: "flex",
                    flexDirection: "column",
                    gap: "24px",
                  }}
                >
                  <div
                    style={{
                      border: "3px solid #191A23",
                      borderRadius: "8px",
                      padding: "20px",
                    }}
                  >
                    <h3
                      style={{
                        fontSize: "1.25rem",
                        fontWeight: "bold",
                        color: "#191A23",
                        marginBottom: "8px",
                      }}
                    >
                      Analysis
                    </h3>
                    <p
                      style={{
                        color: "#191A23",
                        marginBottom: "16px",
                        fontWeight: "500",
                      }}
                    >
                      I is a student
                    </p>

                    <h4
                      style={{
                        fontWeight: "bold",
                        color: "#191A23",
                        marginBottom: "12px",
                        fontSize: "1.1rem",
                      }}
                    >
                      Error cards
                    </h4>

                    <div className="flex flex-col gap-3">
                      <div
                        style={{
                          backgroundColor: "#FFFFFF",
                          border: "3px solid #191A23",
                          borderRadius: "6px",
                          padding: "12px 16px",
                          fontWeight: "600",
                          color: "#191A23",
                          marginBottom: "8px",
                        }}
                      >
                        Subject-Verb Agreement ( is → am)
                      </div>
                      <div
                        style={{
                          backgroundColor: "#FFFFFF",
                          border: "3px solid #191A23",
                          borderRadius: "6px",
                          padding: "12px 16px",
                          fontWeight: "600",
                          color: "#191A23",
                          marginBottom: "8px",
                        }}
                      >
                        Missing Article
                      </div>
                    </div>
                  </div>

                  <div
                    style={{
                      border: "3px solid #191A23",
                      borderRadius: "8px",
                      padding: "20px",
                    }}
                  >
                    <h3
                      style={{
                        fontSize: "1.25rem",
                        fontWeight: "bold",
                        color: "#191A23",
                        marginBottom: "16px",
                      }}
                    >
                      Final Result
                    </h3>
                    <Textarea
                      readOnly
                      placeholder="Peppa Pig..."
                      className="focus-visible:ring-0 focus-visible:ring-offset-0 resize-none"
                      style={{
                        minHeight: "150px",
                        border: "3px solid #191A23",
                        borderRadius: "6px",
                        backgroundColor: "#FFFFFF",
                        color: "#191A23",
                        padding: "16px",
                        fontWeight: "500",
                        fontSize: "1.05rem",
                      }}
                    />
                  </div>
                </div>
              </TabsContent>

              {/* NỘI DUNG TAB: HELP */}
              <TabsContent value="help" className="mt-8 m-0 p-0">
                <div
                  style={{
                    backgroundColor: "#FFFFFF",
                    border: "4px solid #191A23",
                    borderRadius: "8px",
                    boxShadow: "6px 6px 0px 0px #191A23",
                    padding: "24px",
                  }}
                >
                  <h3
                    style={{
                      fontSize: "1.25rem",
                      fontWeight: "bold",
                      color: "#191A23",
                    }}
                  >
                    Help Information
                  </h3>
                  <p
                    style={{
                      marginTop: "16px",
                      color: "#191A23",
                      lineHeight: "1.6",
                      fontWeight: "500",
                    }}
                  >
                    help
                  </p>
                  <p>Grammar DSL command reference.</p>
                  <p>
                    - check grammar *paragraph* <br />
                    - revision plan <br />
                    - history <br />
                    - reset history <br />
                    - spell *word* <br />
                    - verb *word* <br />
                    - synonym *word* <br />
                    - help        <br />
                  </p>
                </div>
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </div>
    </>
  );
}
