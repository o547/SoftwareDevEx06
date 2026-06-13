const language = JSON.parse(document.getElementById("language").textContent);

//google翻訳による言語切り替え
function changeLanguage(language) {
  console.log(`${language}に切り替えます`);
  const select = document.querySelector(".goog-te-combo");

  if (select) {
    select.value = language;
    select.dispatchEvent(new Event("change"));
  }
}

function googleTranslateElementInit() {
  new google.translate.TranslateElement(
    { pageLanguage: "ja" },
    "google_translate_element",
  );
}

changeLanguage(language);
