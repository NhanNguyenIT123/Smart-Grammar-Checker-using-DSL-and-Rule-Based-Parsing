import React from "react";
import GrammarCheckerIllu from "../assets/home/grammarcheckerillu.svg";
import SpellingIllu from "../assets/home/spellingillu.svg";
import StyleEditorIllu from "../assets/home/styleeditorillu.svg";
import PunctuationIllu from "../assets/home/punctuationillu.svg";
import GreenPointer from "../assets/home/greenpointer.svg";
import BlackPointer from "../assets/home/blackpointer.svg";
import StandoutIllu from "../assets/home/standoutillu.svg";

export default function ServicesSection() {
  const basicServices = [
    { title: "Web Browsers" },
    { title: "Office Suites" },
    { title: "Messaging" },
    { title: "Mail" },
  ];

  const featureCards = [
    {
      id: 1,
      title: "Grammar Checker",
      titleBg: "#B9FF66",
      titleColor: "#191A23",
      cardBg: "#F3F3F3",
      learnMoreColor: "#191A23",
      illu: GrammarCheckerIllu,
      pointer: GreenPointer,
    },
    {
      id: 2,
      title: "Spelling",
      titleBg: "#FFFFFF",
      titleColor: "#191A23",
      cardBg: "#B9FF66",
      learnMoreColor: "#191A23",
      illu: SpellingIllu,
      pointer: GreenPointer,
    },
    {
      id: 3,
      title: "Style Editor",
      titleBg: "#FFFFFF",
      titleColor: "#191A23",
      cardBg: "#191A23",
      learnMoreColor: "#FFFFFF",
      illu: StyleEditorIllu,
      pointer: BlackPointer,
    },
    {
      id: 4,
      title: "Punctuation",
      titleBg: "#B9FF66",
      titleColor: "#191A23",
      cardBg: "#F3F3F3",
      learnMoreColor: "#191A23",
      illu: PunctuationIllu,
      pointer: GreenPointer,
    },
  ];

  return (
    <section
      className="w-full font-sans"
      style={{ backgroundColor: "#FFFFFF", padding: "0px 0px 100px 0px" }}
    >
      <div className="max-w-7xl mx-auto">
        {/* --- BASIC SERVICES --- */}
        <div className="flex flex-row flex-wrap justify-between gap-8">
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

        <div style={{ height: "80px", width: "100%" }}></div>

        {/* --- SERVICES --- */}
        <div style={{ paddingLeft: "100px" }}>
          <h2
            className="inline-block px-4 py-2 rounded-xl"
            style={{
              backgroundColor: "#B9FF66",
              color: "#191A23",
              fontWeight: "medium",
              fontSize: "2.25rem",
              lineHeight: "2.5rem",
            }}
          >
            Services
          </h2>
        </div>

        <div style={{ height: "40px", width: "100%" }}></div>

        {/* --- GRID 4 CARD --- */}
        <div
          className="grid grid-cols-2"
          style={{
            gap: "32px",
            paddingLeft: "50px",
            paddingRight: "50px",
            marginBottom: "100px",
          }}
        >
          {featureCards.map((card) => (
            <div
              key={card.id}
              className="overflow-hidden flex flex-row justify-between items-center"
              style={{
                borderRadius: "2.5rem",
                border: "1px solid #191A23",
                height: "350px",
                backgroundColor: card.cardBg,
                boxShadow: "0px 6px 0px 0px #191A23",
                padding: "40px",
              }}
            >
              <div
                className="flex flex-col h-full z-10"
                style={{ width: "50%" }}
              >
                <div>
                  <span
                    className="inline-block px-4 rounded-lg"
                    style={{
                      marginTop: "60px",
                      marginLeft: "60px",
                      fontWeight: "bold",
                      fontSize: "1.25rem",
                      backgroundColor: card.titleBg,
                      color: card.titleColor,
                    }}
                  >
                    {card.title}
                  </span>
                </div>
                <div
                  className="flex items-center gap-3 cursor-pointer"
                  style={{
                    marginTop: "60px",
                    marginLeft: "60px",
                    fontWeight: "bold",
                  }}
                >
                  <img
                    src={card.pointer}
                    className="w-10 h-10"
                    alt=""
                    style={{ objectFit: "contain" }}
                  />
                  <span
                    style={{
                      paddingLeft: "8px",
                      color: card.learnMoreColor,
                      fontSize: "1.25rem",
                    }}
                  >
                    Learn more
                  </span>
                </div>
              </div>
              <div
                className="flex items-center justify-end z-10"
                style={{ width: "30%", height: "100%", marginRight: "40px" }}
              >
                <img
                  src={card.illu}
                  style={{
                    width: "100%",
                    height: "auto",
                    maxHeight: "85%",
                    objectFit: "contain",
                  }}
                  alt=""
                />
              </div>
            </div>
          ))}
        </div>

        <div
          style={{
            padding: "0 50px",
            marginTop: "100px",
          }}
        >
          <div
            style={{
              backgroundColor: "#F3F3F3",
              borderRadius: "2.5rem",
              padding: "60px 80px",
              display: "flex",
              flexDirection: "row",
              justifyContent: "space-between",
              alignItems: "center",
              position: "relative", // Làm mốc cho ảnh absolute
              height: "350px",
            }}
          >
            <div style={{ width: "50%", zIndex: 1 }}>
              <h2
                style={{
                  fontSize: "2.5rem",
                  fontWeight: "bold",
                  color: "#191A23",
                  marginBottom: "24px",
                }}
              >
                Make your writing stand out.
              </h2>
              <p
                style={{
                  fontSize: "1.1rem",
                  color: "#191A23",
                  lineHeight: "1.6",
                  marginBottom: "40px",
                  maxWidth: "450px",
                }}
              >
                Stop worrying about small mistakes and focus on your ideas. Join
                millions of users who improve their writing skills every day
                with our tools.
              </p>
              <button
                style={{
                  backgroundColor: "#191A23",
                  color: "#FFFFFF",
                  padding: "18px 32px",
                  borderRadius: "12px",
                  fontSize: "1.1rem",
                  fontWeight: "bold",
                  cursor: "pointer",
                  border: "none",
                }}
              >
                Join now!!!
              </button>
            </div>

            <div
              style={{
                position: "absolute",
                right: "40px", 
                top: "50%",
                transform: "translateY(-50%)", 
                width: "45%",
                display: "flex",
                justifyContent: "center",
                zIndex: 2, 
              }}
            >
              <img
                src={StandoutIllu}
                style={{
                  width: "400px",
                  maxWidth: "none", 
                  height: "auto",
                  objectFit: "contain",
                  display: "block",
                }}
                alt="Stand out illustration"
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
