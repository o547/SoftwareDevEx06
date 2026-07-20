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

setTimeout(() => {
  changeLanguage(language);
}, 1500);

const alertMessage = JSON.parse(
  document.getElementById("alert_message").textContent,
);

if (alertMessage) {
  alert(alertMessage);
}
const noticesAlertMessage = JSON.parse(
  document.getElementById("notices_alert_message").textContent,
);

if (noticesAlertMessage) {
  alert(noticesAlertMessage);
}

window.addEventListener("pageshow", (event) => {
  if (event.persisted) {
    window.location.reload();
  }
});
