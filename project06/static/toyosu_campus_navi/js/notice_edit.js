const language = JSON.parse(document.getElementById("language").textContent);
//google翻訳による言語切り替え
function googleTranslateElementInit() {
  new google.translate.TranslateElement(
    { pageLanguage: "ja" },
    "google_translate_element",
  );
}
function changeLanguage(language) {
  console.log(`${language}に切り替えます`);
  const select = document.querySelector(".goog-te-combo");

  if (select) {
    select.value = language;
    select.dispatchEvent(new Event("change"));
  }
}

changeLanguage(language);

//お知らせを投稿(編集)
async function submitNotice(language) {
  const title = document.querySelector(".edit-title-input").value;
  const body = document.querySelector(".edit-content-input").value;

  if (title.length == 0) {
    alert("タイトルがありません");
    return;
  }
  if (title.length > 128) {
    alert("タイトルは128文字未満で入力してください");
    return;
  }
  if (body.length == 0) {
    alert("本文がありません");
    return;
  }

  const url = new URL(window.location.href);
  const params = url.searchParams;
  const notice_id = params.get("notice_id");

  //Ajax通信で返答を取得
  const response = await fetch("/notice/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
    body: JSON.stringify({
      title: title,
      body: body,
      notice_id: notice_id,
    }),
  });

  const data = await response.json();
  if (data.alert_message) {
    alert(data.alert_message);
  } else if (response.ok) {
    window.location.href = "/notice/management";
  }
}

const alertMessage = JSON.parse(
  document.getElementById("alert_message").textContent,
);

if (alertMessage) {
  alert(alertMessage);
}
const currentNotice = JSON.parse(
  document.getElementById("current_notice").textContent,
);

if (currentNotice.alert_message) {
  alert(currentNotice.alert_message);
}

changeLanguage(language);
