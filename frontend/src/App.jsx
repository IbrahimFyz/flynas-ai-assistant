import { useState } from "react";
import "./App.css";

const quickActions = [
  {
    icon: "✈",
    title: "حجز رحلة",
    description: "ابحث عن الرحلات والأسعار",
    prompt: "What flights are available?",
  },
  {
    icon: "▣",
    title: "إدارة الحجز",
    description: "تعديل أو إلغاء حجزك",
    prompt: "How can I change my booking?",
  },
  {
    icon: "▤",
    title: "الأمتعة",
    description: "الوزن المسموح والخيارات",
    prompt: "What baggage can I take?",
  },
  {
    icon: "▥",
    title: "إجراءات السفر",
    description: "المستندات والمتطلبات",
    prompt: "What travel documents do I need?",
  },
  {
    icon: "＋",
    title: "خدمات إضافية",
    description: "اختر خدمات أو وجبات",
    prompt: "What additional services are available?",
  },
];


// =========================
// CLEAN MARKDOWN
// =========================

function cleanInlineText(text) {
  if (!text) return "";

  return text
    .replace(/\*\*(.*?)\*\*/g, "$1")
    .replace(/__(.*?)__/g, "$1")
    .replace(/`(.*?)`/g, "$1")
    .replace(/^#{1,6}\s*/g, "")
    .trim();
}


// =========================
// TABLE DETECTION
// =========================

function isTableSeparator(line) {
  return /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(
    line
  );
}


function parseTableRow(line) {
  return line
    .trim()
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map((cell) => cleanInlineText(cell));
}


// =========================
// RESPONSE RENDERER
// =========================

function renderResponse(text, darkMode) {
  if (!text) return null;

  const normalizedText = text
    .replace(/\r\n/g, "\n")
    .replace(/\r/g, "\n");

  let lines = normalizedText.split("\n");

  /*
    Sometimes the AI returns the whole Markdown table
    in one line.

    Example:
    | A | B | |---|---| | X | Y | | Z | W |

    Try to separate the rows automatically.
  */

  if (
    lines.length === 1 &&
    normalizedText.includes("|") &&
    normalizedText.includes("---")
  ) {
    lines = normalizedText
      .replace(/\|\s*\|(?=\s*[-:])/g, "|\n|")
      .replace(/\|\s*\|(?=\s*[A-Za-z\u0600-\u06FF])/g, "|\n|")
      .split("\n");
  }

  const elements = [];

  let i = 0;

  while (i < lines.length) {
    const line = lines[i].trim();

    if (!line) {
      i++;
      continue;
    }


    // =========================
    // TABLE
    // =========================

    if (
      line.includes("|") &&
      i + 1 < lines.length &&
      isTableSeparator(lines[i + 1])
    ) {
      const headers = parseTableRow(line);

      const rows = [];

      i += 2;

      while (
        i < lines.length &&
        lines[i].includes("|") &&
        lines[i].trim()
      ) {
        rows.push(parseTableRow(lines[i]));
        i++;
      }

      elements.push(
        <div
          key={`table-${i}`}
          style={{
            width: "100%",
            overflowX: "auto",
            margin: "12px 0",
            borderRadius: "12px",
          }}
        >
          <table
            style={{
              width: "100%",
              borderCollapse: "separate",
              borderSpacing: 0,
              overflow: "hidden",
              fontSize: "14px",
              textAlign: "right",
              direction: "rtl",
            }}
          >
            <thead>
              <tr>
                {headers.map((header, index) => (
                  <th
                    key={index}
                    style={{
                      padding: "11px 13px",
                      fontWeight: 700,
                      borderBottom: darkMode
                        ? "1px solid rgba(255,255,255,0.12)"
                        : "1px solid rgba(0,0,0,0.1)",
                      background: darkMode
                        ? "rgba(255,255,255,0.07)"
                        : "rgba(0,0,0,0.05)",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {header}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              {rows.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {headers.map((_, cellIndex) => (
                    <td
                      key={cellIndex}
                      style={{
                        padding: "10px 13px",
                        borderBottom:
                          rowIndex === rows.length - 1
                            ? "none"
                            : darkMode
                            ? "1px solid rgba(255,255,255,0.08)"
                            : "1px solid rgba(0,0,0,0.08)",
                        background:
                          rowIndex % 2 === 0
                            ? darkMode
                              ? "rgba(255,255,255,0.025)"
                              : "rgba(0,0,0,0.015)"
                            : "transparent",
                        whiteSpace: "nowrap",
                      }}
                    >
                      {row[cellIndex] || ""}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );

      continue;
    }


    // =========================
    // BULLET LIST
    // =========================

    if (/^[-*•]\s+/.test(line)) {
      const bulletItems = [];

      while (
        i < lines.length &&
        /^[-*•]\s+/.test(lines[i].trim())
      ) {
        bulletItems.push(
          lines[i]
            .trim()
            .replace(/^[-*•]\s+/, "")
        );

        i++;
      }

      elements.push(
        <ul
          key={`list-${i}`}
          style={{
            margin: "8px 0",
            paddingRight: "22px",
            lineHeight: 1.9,
          }}
        >
          {bulletItems.map((item, index) => (
            <li key={index}>
              {cleanInlineText(item)}
            </li>
          ))}
        </ul>
      );

      continue;
    }


    // =========================
    // NORMAL TEXT
    // =========================

    elements.push(
      <div
        key={`text-${i}`}
        style={{
          lineHeight: 1.8,
          marginBottom: "4px",
        }}
      >
        {cleanInlineText(line)}
      </div>
    );

    i++;
  }

  return elements;
}


function App() {
  const [darkMode, setDarkMode] = useState(true);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);


  const sendMessage = async () => {
    const trimmedMessage = message.trim();

    if (!trimmedMessage) return;

    setMessages((current) => [
      ...current,
      {
        role: "user",
        content: trimmedMessage,
      },
    ]);

    setMessage("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: trimmedMessage,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Backend request failed");
      }

      const data = await response.json();

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content:
            data.response ||
            "عذرًا، لم أتمكن من الحصول على إجابة.",
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content:
            "عذرًا، حدث خطأ أثناء الاتصال بالمساعد. تأكد من أن الخادم يعمل.",
        },
      ]);
    }
  };


  const useQuickAction = (prompt) => {
    setMessage(prompt);
  };


  const startNewChat = () => {
    setMessages([]);
    setMessage("");
  };


  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };


  return (
    <div
      className={`app ${darkMode ? "dark" : "light"}`}
      dir="rtl"
    >

      {/* =========================
          LEFT SIDEBAR
      ========================== */}

      <aside className="sidebar sidebar-left">

        <div className="brand">
          <div className="brand-logo">
            <div>
              <div className="brand-name">flynas</div>
              <div className="brand-arabic">طيران ناس</div>
            </div>
          </div>
        </div>


        {/* Services */}

        <div className="services-section">

          <div className="services-title">
            الخدمات
          </div>

          <div className="services-list">

            {quickActions.map((action) => (
              <button
                className="service-item"
                key={action.title}
                onClick={() =>
                  useQuickAction(action.prompt)
                }
              >
                <div className="service-icon">
                  {action.icon}
                </div>

                <div className="service-content">
                  <strong>{action.title}</strong>
                  <span>{action.description}</span>
                </div>
              </button>
            ))}

          </div>
        </div>


        {/* Online Assistant */}

        <div className="sidebar-bottom">

          <div className="online-card">

            <span className="headset">
              ♧
            </span>

            <div>
              <strong>المساعد متصل</strong>
              <small>متاح لمساعدتك 7/24</small>
            </div>

            <span className="online-dot"></span>

          </div>

        </div>

      </aside>


      {/* =========================
          MAIN CHAT AREA
      ========================== */}

      <main className="main-area">

        <div
          className="cabin-background"
          style={{
            backgroundImage: `url(${
              darkMode
                ? "/cabin-dark.png"
                : "/cabin-light.png"
            })`,
          }}
        />

        <div className="cabin-overlay" />


        {/* Top Header */}

        <header className="top-bar">

          <div className="page-title">
            مرحبًا، كيف أقدر{" "}
            <span>أساعدك</span>{" "}
            اليوم؟
          </div>

          <div className="top-controls">

            <button
              className="theme-button"
              onClick={() =>
                setDarkMode(
                  (current) => !current
                )
              }
              aria-label="Toggle theme"
            >
              {darkMode ? "☀" : "☾"}
            </button>

            <button className="language-button">
              EN
            </button>

          </div>

        </header>


        {/* Conversation */}

        <section className="conversation">

          {messages.length > 0 && (

            <div className="messages">

              {messages.map(
                (item, index) => (

                  <div
                    className={`message-row ${
                      item.role === "user"
                        ? "user-row"
                        : "assistant-row"
                    }`}
                    key={index}
                  >

                    <div
                      className={
                        item.role === "user"
                          ? "user-message"
                          : "assistant-message"
                      }
                    >

                      {item.role === "assistant"
                        ? renderResponse(
                            item.content,
                            darkMode
                          )
                        : item.content}

                    </div>

                  </div>

                )
              )}

            </div>

          )}

        </section>


        {/* Input */}

        <div className="chat-input-wrapper">

          <button
            className="attachment-button"
            aria-label="Attach file"
          >
            📎
          </button>

          <textarea
            value={message}
            onChange={(event) =>
              setMessage(event.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder="اكتب سؤالك هنا..."
            rows="1"
          />

          <button
            className="send-button"
            onClick={sendMessage}
            aria-label="Send message"
          >
            ↑
          </button>

        </div>


        {/* Disclaimer */}

        <div className="disclaimer">

          <span>◉</span>

          قد يخطئ المساعد في بعض المعلومات.
          تأكد من التفاصيل المهمة قبل سفرك.

        </div>

      </main>


      {/* =========================
          RIGHT SIDEBAR
      ========================== */}

      <aside className="sidebar sidebar-right">

        <button
          className="new-chat-button right-new-chat"
          onClick={startNewChat}
        >

          <span className="button-plus">
            ＋
          </span>

          <div className="new-chat-content">
            <strong>محادثة جديدة</strong>
            <small>متاح لمساعدتك 7/24</small>
          </div>

        </button>


        {/* Destination */}

        <div className="destination-card">

          <span className="destination-label">
            اكتشف أكثر من
          </span>

          <strong>
            85+ وجهة
          </strong>

          <p>
            في الشرق الأوسط، آسيا، أوروبا
            <br />
            وأفريقيا
          </p>

          <button>
            استكشف الوجهات
          </button>

        </div>


        {/* Journey */}

        <div className="journey-card">

          <div className="journey-icon">
            ✈
          </div>

          <div>

            <strong>
              رحلتك تبدأ من هنا
            </strong>

            <p>
              اسألني عن أي شيء يخص سفرك.
            </p>

          </div>

        </div>

      </aside>

    </div>
  );
}

export default App;