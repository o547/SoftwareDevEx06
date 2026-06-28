//モーダルを活性にする
function openModal(targetMenuId) {
  document.getElementById(targetMenuId).style.display = "contents";
  document.getElementById("modal").classList.add("active");
}

//モーダルを非活性にする
function closeModal() {
  const modalMenus = document.querySelectorAll(".modal-menu");
  for (const modalMenu of modalMenus) {
    modalMenu.style.display = "none";
  }
  document.getElementById("modal").classList.remove("active");
}

//第一引数のメニューを非表示にして、第二引数のメニューを表示する。
function toggleMenu(currentMenuId, targetMenuId, displayMethod) {
  document.getElementById(currentMenuId).style.display = "none";
  document.getElementById(targetMenuId).style.display = displayMethod;

  const notice = document.getElementById("sidebar-notice");

  if (targetMenuId === "sidebar-login") {
    notice.style.display = "none";
  }

  if (targetMenuId === "sidebar-buttons") {
    notice.style.display = "flex";
  }
}

//サイドバーを閉じる
function closeSidebar(sidebarId, buttonId) {
  const sidebar = document.getElementById(sidebarId);
  const openButton = document.getElementById(buttonId);
  sidebar.classList.add("closed");
  sidebar.style.width = "0";
  openButton.classList.add("active");
}

//サイドバーを開く
function openSidebar(sidebarId, buttonId) {
  const sidebar = document.getElementById(sidebarId);
  const openButton = document.getElementById(buttonId);
  sidebar.classList.remove("closed");
  sidebar.style.width = "300px";
  openButton.style.width = "0";
  openButton.classList.remove("active");
}

//ログインまたは新規登録のデータを送信
function submitLogin(parentId) {
  const parentDiv = document.getElementById(parentId);
  const username = parentDiv.querySelector("#login-id").value;
  const usernameRegex = /^[A-Za-z0-9_@.+-]{1,150}$/;

  if (!usernameRegex.test(username)) {
    alert(
      "usernameは150文字以下の半角英数字および記号(_@.+-)で入力してください",
    );
    return;
  }

  const password = parentDiv.querySelector("#login-password").value;
  const passwordRegex = /^[!-~]{1,128}$/;

  if (!passwordRegex.test(password)) {
    alert("パスワードは128文字以下の半角英数字および記号で入力してください");
    return;
  }

  const form = parentDiv.querySelector("form");
  form.action = "/user/login";
  form.method = "post";
  form.requestSubmit();
}

//チャットボットに質問をする
async function chatbotSubmit() {
  const conversationArea = document.querySelector(".chatbot-conversation");
  const chatbotInput = document.querySelector(".chatbot-input");
  const chatbotInputValue = document.querySelector(".chatbot-input").value;

  if (!chatbotInputValue) {
    alert("質問を入力してください");
    return;
  }
  if (chatbotInputValue.length > 200) {
    alert("200文字以下で入力してください");
    return;
  }

  //ユーザの質問文を描画
  conversationArea.insertAdjacentHTML(
    "beforeend",
    `<div class="chat-row user-row">
      <div class="chatbot-message user-message notranslate">${chatbotInputValue}</div>
    </div>`,
  );

  //テキストボックスをクリア
  chatbotInput.value = "";

  const botIconSrc = document.querySelector(".bot-icon").src;
  conversationArea.insertAdjacentHTML(
    "beforeend",
    `<div class="chat-row bot-row bot-loading">
      <img src="${botIconSrc}" class="bot-icon">
      <div class="chatbot-message bot-message">メッセージを生成中...</div>
    </div>`,
  );

  conversationArea.scrollTop = conversationArea.scrollHeight;

  //Ajax通信で返答を取得
  const response = await fetch("/chatbot/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
    body: JSON.stringify({
      question: chatbotInputValue,
    }),
  });

  const data = await response.json();
  document.querySelector(".bot-loading").remove();
  if (data.alert_message) {
    alert(data.alert_message);

    if (!data.chatbot_response) {
      return;
    }
  }

  //返答文を描画
  conversationArea.insertAdjacentHTML(
    "beforeend",
    `<div class="chat-row bot-row">
      <img src="${botIconSrc}" class="bot-icon">
      <div class="chatbot-message bot-message">${data.chatbot_response}</div>
    </div>`,
  );

  //最後までスクロール
  conversationArea.scrollTop = conversationArea.scrollHeight;
}

function createPostJson(key, value) {
  return {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
    body: JSON.stringify({
      [key]: value,
    }),
  };
}

//言語設定を変更して保存する
async function selectLanguage(language) {
  //Ajax通信で返答を取得
  const response = await fetch(
    "/language/submit",
    createPostJson("language", language),
  );
  const data = await response.json();
  if (data.alert_message) {
    alert(data.alert_message);
  }
  await changeLanguage(language);
  await changeLanguage(language);
}

//スタート地点またはゴール地点を決定
function searchEnter(direction) {
  //検索メニューの表記を変更
  const startPointMenuButton = document.getElementById(
    "start-point-menu-button",
  );
  const goalPointMenuButton = document.getElementById("goal-point-menu-button");
  if (startSectionSelect.value) {
    startPointMenuButton.innerText = startSectionSelect.value;
    startPointMenuButton.style.fontSize = "0.9rem";
  } else {
    startPointMenuButton.innerText = "出発地";
    startPointMenuButton.style.fontSize = "1rem";
  }
  if (goalSectionSelect.value) {
    goalPointMenuButton.innerText = goalSectionSelect.value;
    goalPointMenuButton.style.fontSize = "1rem";
  } else {
    goalPointMenuButton.innerText = "目的地";
    goalPointMenuButton.style.fontSize = "1rem";
  }

  if (!startSectionSelect.value || !goalSectionSelect.value) {
    toggleMenu(`${direction}-point-menu`, "search-menu", "contents");
    return;
  }
  //検索を実行
  location.href = `/search/${encodeURIComponent(startSectionSelect.value)}/${encodeURIComponent(goalSectionSelect.value)}`;
}

//画像クリックで区画情報を取得
async function sectionCoordinateSubmit(image_x, image_y) {
  //Ajax通信で返答を取得
  const map_name = currentWing + "_" + currentFloorNumber + "階";
  const response = await fetch("/coordinate/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
    body: JSON.stringify({
      image_x: image_x,
      image_y: image_y,
      map_name: map_name,
    }),
  });
  const data = await response.json();
  if (data.section) {
    console.log(data);

    if (selectFromMapMode) {
      const wingSelectBox = document.getElementById(
        `${selectFromMapDirection}-wing-select`,
      );
      wingSelectBox.value = currentWing;

      const floorSelectBox = document.getElementById(
        `${selectFromMapDirection}-floor-select`,
      );
      floorSelectBox.value = currentFloorNumber + "階";

      const sectionSelectBox = document.getElementById(
        `${selectFromMapDirection}-section-select`,
      );
      sectionSelectBox.value = `${currentWing}_${currentFloorNumber}階_${data.section}`;

      selectFromMapMode = false;
      openModal(`${selectFromMapDirection}-point-menu`);
    } else {
      openSectionModal(
        data.section,
        data.usage,
        data.capacity,
        data.business_hours,
      );
    }
  }
}

//詳細表示モーダルを活性にする
function openSectionModal(section, usage, capacity, business_hours) {
  const sectionModalNameElement = document.querySelector(".section-modal-name");
  const sectionModalBodyElement = document.querySelector(".section-modal-body");
  sectionModalNameElement.innerHTML = section.replace("区画調整", "");

  if (section.length > 20) {
    sectionModalNameElement.style.fontSize = "1rem";
  } else if (section.length > 15) {
    sectionModalNameElement.style.fontSize = "1.2rem";
  } else {
    sectionModalNameElement.style.fontSize = "1.4rem";
  }

  let sectionInfo = "";
  if (!usage && capacity == -1 && !business_hours) {
    sectionInfo = "情報は登録されていません";
  } else {
    if (usage) {
      sectionInfo += `<div>主な用途：${usage}</div>`;
    }
    if (capacity != -1) {
      sectionInfo += `<div>収容人数：${capacity}人</div>`;
    }
    if (business_hours) {
      sectionInfo += `<div>営業時間：${business_hours}</div>`;
    }
  }

  sectionModalBodyElement.innerHTML = sectionInfo;
  document.querySelector(".section-modal").classList.add("active");
}

//詳細表示モーダルを非活性にする
function closeSectionModal() {
  if (event.target == event.currentTarget) {
    document.querySelector(".section-modal").classList.remove("active");
  }
}

function toggleLanguageMenu() {
  const menu = document.getElementById("sidebar-language-menu");
  menu.classList.toggle("active");
  document.addEventListener("click", removeLanguageMenuActive);
}

function closeLanguageMenu() {
  document.getElementById("sidebar-language-menu").classList.remove("active");
}

function removeLanguageMenuActive(event) {
  const menu = document.getElementById("sidebar-language-menu");

  if (!menu) return;

  const button = event.target.closest("#language-button");
  const insideMenu = event.target.closest("#sidebar-language-menu");

  if (!insideMenu && !button) {
    menu.classList.remove("active");
    document.removeEventListener("click", removeLanguageMenuActive);
  }
}
function getCurrentPositionPromise() {
  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(resolve, reject);
  });
}

function getCurrentPositionPromise() {
  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(resolve, reject);
  });
}

async function getLocation() {
  if (!navigator.geolocation) {
    return {
      latitude: -91,
      longitude: -181,
    };
  }
  try {
    const position = await getCurrentPositionPromise();
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    return {
      latitude: latitude,
      longitude: longitude,
    };
  } catch (error) {
    console.log(error);
    return {
      latitude: -91,
      longitude: -181,
    };
  }
}

async function getWingNameByLocation() {
  const location = await getLocation();

  //Ajax通信で返答を取得
  const response = await fetch("/identify/wing", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
    body: JSON.stringify({
      latitude: location.latitude,
      longitude: location.longitude,
    }),
  });
  const data = await response.json();
  return data.wing_name;
}

async function changeWingByLocation() {
  const wingGPSButton = document.querySelector(".wing-gps-button");
  wingGPSButton.innerText = "位置を取得中...";
  const wingName = await getWingNameByLocation();

  if (wingName) {
    for (const wingSwitch of wingSwitches) {
      if (wingSwitch.value == wingName) {
        wingSwitch.checked = true;
        changeWing(wingSwitch.value, wingSwitch);
      } else {
        wingSwitch.checked = false;
        if (!isFloorMapMode) {
          changeWing(wingSwitch.value, wingSwitch);
        }
      }
    }
    wingGPSButton.innerText = `GPSから取得 (${wingName})`;
  } else {
    wingGPSButton.innerHTML = `GPSから取得 (失敗))`;
    alert("現在いる棟を取得できませんでした。手動で入力をしてください。");
  }
}

//選択メニューの「GPSから取得」
async function changeSelectOptionByLocation(buttonElement, targetInputId) {
  const targetInput = document.getElementById(targetInputId);
  buttonElement.innerText = "位置を取得中...";

  const wingName = await getWingNameByLocation();
  if (wingName) {
    targetInput.value = wingName;
    const event = new Event("change");
    targetInput.dispatchEvent(event);
    buttonElement.innerText = `GPSから推定 (${wingName})`;
  } else {
    buttonElement.innerText = `GPSから推定 (失敗)`;
  }
}

let selectFromMapMode = false;
let selectFromMapDirection = null;
//検索メニューの「地図から取得」
function selectFromMap(direction) {
  selectFromMapMode = true;
  selectFromMapDirection = direction;
  if (!isFloorMapMode) {
    const switchElement = document.querySelector(".dimention-switch-switch");
    toggleDimention(switchElement);
  }
  closeModal();
}

//検索メニューの「決定」ボタンを必要であれば「検索」に変える
function toggleSearchEnterButton(direction) {
  let oppositeSectionSelect = null;
  if (direction == "start") {
    oppositeSectionSelect = document.getElementById("goal-section-select");
  } else {
    oppositeSectionSelect = document.getElementById("start-section-select");
  }
  let enterButton = document.getElementById(`${direction}-point-enter-button`);
  if (oppositeSectionSelect.value) {
    enterButton.innerText = "検索";
  } else {
    enterButton.innerText = "決定";
  }
}

//検索メニューの選択肢制御
function controlSearchMenu(selectBoxId) {
  if (selectBoxId == "start-wing-select" || selectBoxId == "goal-wing-select") {
    const selectedWingName = document.getElementById(selectBoxId).value;
    //階を制御
    let floorSelect = null;
    if (selectBoxId == "start-wing-select") {
      floorSelect = document.getElementById("start-floor-select");
    } else {
      floorSelect = document.getElementById("goal-floor-select");
    }
    const floorSelectOptions = floorSelect.querySelectorAll(
      "option[value]:not([value='']",
    );
    for (const floorSelectOption of floorSelectOptions) {
      if (selectedWingName) {
        if (
          wingFloors[selectedWingName].includes(
            String(floorSelectOption.value).slice(0, -1),
          )
        ) {
          floorSelectOption.style.display = "";
        } else {
          floorSelectOption.style.display = "none";
          if (floorSelectOption.value == floorSelect.value) {
            floorSelect.value = "";
          }
        }
      } else {
        floorSelectOption.style.display = "";
      }
    }

    //区画を制御
    let sectionSelect = null;
    if (selectBoxId == "start-wing-select") {
      sectionSelect = document.getElementById("start-section-select");
    } else {
      sectionSelect = document.getElementById("goal-section-select");
    }
    const sectionSelectOptions = sectionSelect.querySelectorAll(
      "option[value]:not([value='']",
    );
    for (const sectionSelectOption of sectionSelectOptions) {
      if (selectedWingName) {
        if (sectionSelectOption.dataset.wing == selectedWingName) {
          sectionSelectOption.style.display = "";
        } else {
          sectionSelectOption.style.display = "none";
          if (sectionSelectOption.value == sectionSelect.value) {
            sectionSelect.value = "";
          }
        }
      } else {
        sectionSelectOption.style.display = "";
      }
    }
  } else if (
    selectBoxId == "start-floor-select" ||
    selectBoxId == "goal-floor-select"
  ) {
    const selectedFloor = document.getElementById(selectBoxId).value;
    let sectionSelect = null;
    if (selectBoxId == "start-floor-select") {
      sectionSelect = document.getElementById("start-section-select");
    } else {
      sectionSelect = document.getElementById("goal-section-select");
    }
    const sectionSelectOptions = sectionSelect.querySelectorAll(
      "option[value]:not([value='']",
    );
    //区画を制御
    for (const sectionSelectOption of sectionSelectOptions) {
      if (selectedFloor) {
        if (sectionSelectOption.dataset.floor == selectedFloor) {
          sectionSelectOption.style.display = "";
        } else {
          sectionSelectOption.style.display = "none";
          if (sectionSelectOption.value == sectionSelect.value) {
            sectionSelect.value = "";
          }
        }
      } else {
        sectionSelectOption.style.display = "";
      }
    }
  } else if (
    selectBoxId == "start-section-select" ||
    selectBoxId == "goal-section-select"
  ) {
    const selectedOption =
      document.getElementById(selectBoxId).selectedOptions[0];
    if (selectBoxId == "start-section-select") {
      document.getElementById("start-wing-select").value =
        selectedOption.dataset.wing;
      document.getElementById("start-floor-select").value =
        selectedOption.dataset.floor;
    } else {
      document.getElementById("goal-wing-select").value =
        selectedOption.dataset.wing;
      document.getElementById("goal-floor-select").value =
        selectedOption.dataset.floor;
    }
  }
}

//---------------地図切り替え処理 開始---------------

let currentWing = "教室棟";
let currentFloorNumber = 1;
let isFloorMapMode = false;
const floorSelectMenu = document.getElementById("floor-select-menu");
const wingSwitches = document.querySelectorAll(".wing-switch");
const floorMapImageArea = document.getElementById("floor-map-image-area");
const wholeMapImageArea = document.getElementById("whole-map-image-area");
const floorMapImage = document.getElementById("floor-map-img");
const campusMapImageArea = document.querySelector(".campus-img-area");
const campusMapImage = document.getElementById("campus-img");

const wholeMapImages = {
  本部棟: document.querySelector('.map-scroll[data-wing="本部棟"]'),
  教室棟: document.querySelector('.map-scroll[data-wing="教室棟"]'),
  交流棟: document.querySelector('.map-scroll[data-wing="交流棟"]'),
  研究棟: document.querySelector('.map-scroll[data-wing="研究棟"]'),
};

const wingFloors = {
  教室棟: ["1", "2", "3", "4", "5", "6", "7"],
  交流棟: ["1", "2", "3", "4", "5", "6"],
  研究棟: [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
  ],
  本部棟: [
    "B1",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
  ],
};

//campusMapの座標と該当する棟（左上，右下，棟）
const campusMapCoordinates = [
  [[298, 84], [1827, 487], "研究棟"],
  [[559, 495], [1732, 571], "研究棟"],
  [[950, 692], [1268, 943], "研究棟"],
  [[1430, 726], [1680, 1178], "研究棟"],
  [[308, 497], [555, 1157], "教室棟"],
  [[33, 657], [878, 1028], "教室棟"],
  [[459, 1288], [748, 2018], "交流棟"],
  [[88, 1377], [890, 1701], "交流棟"],
  [[1093, 1366], [1959, 1796], "本部棟"],
  [[919, 1589], [1420, 2250], "本部棟"],
];

//表示階を変更
function changeFloor(floorNumber) {
  currentFloorNumber = floorNumber;
  if (
    createdMapFiles &&
    createdMapFiles.includes(`${currentWing}_${floorNumber}階_route.jpg`)
  ) {
    floorMapImage.src = floorMapImage.src.replace(
      /floor_map\/.*/,
      `floor_map/created_maps/${createdMapFolderName}/${currentWing}_${floorNumber}階_route.jpg`,
    );
  } else {
    floorMapImage.src = floorMapImage.src.replace(
      /floor_map\/.*/,
      `floor_map/${currentWing}_${floorNumber}階.jpg`,
    );
  }

  const floorSelectElements = floorSelectMenu.querySelectorAll(".floor-select");
  for (const floorSelectElement of floorSelectElements) {
    if (floorSelectElement.innerText == floorNumber) {
      floorSelectElement.style.color = "rgb(0, 0, 0)";
      floorSelectElement.style.fontWeight = "bold";
    } else {
      floorSelectElement.style.color = "rgb(90, 90, 90)";
      floorSelectElement.style.fontWeight = "normal";
    }
  }
}

//平面立体を変更
function toggleDimention(switchElement) {
  isFloorMapMode = !isFloorMapMode;
  const thumbElement = switchElement.querySelector(".dimention-switch-thumb");
  if (isFloorMapMode) {
    //立体→平面
    thumbElement.classList.remove("right");
    thumbElement.classList.add("left");
    floorSelectMenu.style.visibility = "";
    campusMapImageArea.style.display = "none";
    let firstChecked = true;
    let firstCheckedWing = "";
    //どの棟がチェックされているかを確認
    for (const wingSwitch of wingSwitches) {
      if (wingSwitch.checked) {
        if (firstChecked) {
          firstCheckedWing = wingSwitch.value;
          firstChecked = false;
        } else {
          wingSwitch.checked = false;
        }
      }
      wingSwitch.type = "radio";
    }
    floorMapImageArea.style.display = "";
    wholeMapImageArea.style.display = "none";
    panzoom.reset();
    if (firstCheckedWing) {
      changeWing(firstCheckedWing);
    } else {
      //一つもチェックがされていない
      for (const wingSwitch of wingSwitches) {
        if (wingSwitch.value == "教室棟") {
          wingSwitch.checked = true;
        }
      }
      changeWing("教室棟");
    }
  } else {
    //平面→立体
    thumbElement.classList.remove("left");
    thumbElement.classList.add("right");
    floorSelectMenu.style.visibility = "hidden";
    floorMapImageArea.style.display = "none";
    wholeMapImageArea.style.display = "";
    for (const wingSwitch of wingSwitches) {
      wingSwitch.type = "checkbox";
      changeWing(wingSwitch.value, wingSwitch);
    }
  }
}

//棟を変更
function changeWing(wingName, inputElement) {
  // console.log(wingName, inputElement.checked);
  if (isFloorMapMode) {
    currentWing = wingName;
    //階選択メニューを変更
    const floorSelectElements = document.querySelectorAll(".floor-select");
    for (const floorSelectElement of floorSelectElements) {
      if (wingFloors[wingName].includes(floorSelectElement.innerText)) {
        floorSelectElement.style.display = "";
      } else {
        floorSelectElement.style.display = "none";
      }
    }
    if (wingFloors[wingName].includes(currentFloorNumber)) {
      //選択されていた階に切り替える
      changeFloor(currentFloorNumber);
    } else {
      //選択されていた階が存在しなければ1階にする
      changeFloor(1);
    }
    panzoom.reset();
    if (wingName == "研究棟") {
      floorMapImage.classList.remove("other-floor-map");
      floorMapImage.classList.add("research-building-floor-map");
    } else {
      floorMapImage.style.height = floorMapImage.classList.remove(
        "research-building-floor-map",
      );
      floorMapImage.classList.add("other-floor-map");
    }
  } else {
    if (inputElement && inputElement.checked) {
      wholeMapImages[wingName].style.display = "block";
      wholeMapImages[wingName].scrollTop =
        wholeMapImages[wingName].scrollHeight;
      campusMapImageArea.style.display = "none";
    } else {
      wholeMapImages[wingName].style.display = "none";
      //全てチェックされていなければキャンパス全体を表示
      let noChecks = true;
      for (const wingSwitch of wingSwitches) {
        if (wingSwitch.checked) {
          noChecks = false;
        }
      }
      if (noChecks) {
        campusMapImageArea.style.display = "";
      } else {
        campusMapImageArea.style.display = "none";
      }
    }
  }
}

//---------------地図切り替え処理 終了---------------

function googleTranslateElementInit() {
  new google.translate.TranslateElement(
    { pageLanguage: "ja" },
    "google_translate_element",
  );
}

//google翻訳による言語切り替え
function changeLanguage(language) {
  console.log(`${language}に切り替えます`);
  const select = document.querySelector(".goog-te-combo");

  if (select) {
    select.value = language;
    select.dispatchEvent(new Event("change"));
  }
  setTimeout(() => {
    translateWingNames(language);
  }, 1000);
}
const wingTranslations = {
  en: {
    本部棟: "Centennial Main Building",
    教室棟: "Classroom & Administration Building",
    交流棟: "Multi-Activity Building",
    研究棟: "Research Building",
  },
  "zh-CN": {
    本部棟: "总部楼",
    教室棟: "教学楼",
    交流棟: "交流楼",
    研究棟: "研究楼",
  },
  ja: {
    本部棟: "本部棟",
    教室棟: "教室棟",
    交流棟: "交流棟",
    研究棟: "研究棟",
  },
};
function translateWingNames(language) {
  const names = document.querySelectorAll(".wing-name");

  names.forEach((element) => {
    const wing = element.dataset.wing;

    element.textContent = wingTranslations[language][wing];
  });
}

//サーバーから変数を受け取る
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

const username = JSON.parse(document.getElementById("username").textContent);

const is_superuser = JSON.parse(
  document.getElementById("is_superuser").textContent,
);

if (is_superuser == true) {
  console.log("管理者でログイン");
}

let language = JSON.parse(document.getElementById("language").textContent);
if (!language) {
  language = "ja";
}

const sectionNames = JSON.parse(
  document.getElementById("section_names").textContent,
);

const route = JSON.parse(document.getElementById("route").textContent);

const createdMapFiles = JSON.parse(
  document.getElementById("map_files").textContent,
);

const createdMapFolderName = JSON.parse(
  document.getElementById("map_folder_name").textContent,
);

//panzoom
const panzoom = Panzoom($("#floor-map-img")[0], {
  maxScale: 5,
  minScale: 0.05,

  contain: null,
});

// ホイールズーム
document
  .querySelector(".viewer")
  .addEventListener("wheel", panzoom.zoomWithWheel);

//クリックかドラッグかの判定
let isDragging = false;
let dragStartX = 0;
let dragStartY = 0;
floorMapImage.addEventListener("pointerdown", (event) => {
  if (event.pointerType === "mouse" && event.button !== 0) {
    return;
  }
  dragStartX = event.clientX;
  dragStartY = event.clientY;
  isDragging = false;
});

floorMapImage.addEventListener("pointermove", (event) => {
  if (event.pressure === 0) {
    return;
  }
  const moveX = Math.abs(event.clientX - dragStartX);
  const moveY = Math.abs(event.clientY - dragStartY);
  if (moveX > 5 || moveY > 5) {
    isDragging = true;
  }
});

floorMapImage.addEventListener("pointerup", () => {
  setTimeout(() => {
    isDragging = false;
  }, 0);
});

//画像クリックで座標を送信
floorMapImage.addEventListener("click", async (event) => {
  if (isDragging) {
    return;
  }
  const initialDisplayWidth = floorMapImage.offsetWidth;
  const initialDisplayHeight = floorMapImage.offsetHeight;
  const naturalWidth = floorMapImage.naturalWidth;
  const naturalHeight = floorMapImage.naturalHeight;
  const rect = floorMapImage.getBoundingClientRect();

  const scale = panzoom.getScale();

  // CSS適用後のサイズとnaturalサイズの比率を計算
  const scaleX = naturalWidth / initialDisplayWidth;
  const scaleY = naturalHeight / initialDisplayHeight;

  let x = Math.round(((event.clientX - rect.left) / scale) * scaleX);
  let y = Math.round(((event.clientY - rect.top) / scale) * scaleY);
  sectionCoordinateSubmit(x, y);
});

//全体地図クリックで棟を選択
campusMapImage.addEventListener("click", async (event) => {
  if (isDragging) {
    return;
  }
  const initialDisplayWidth = campusMapImage.offsetWidth;
  const initialDisplayHeight = campusMapImage.offsetHeight;
  const naturalWidth = campusMapImage.naturalWidth;
  const naturalHeight = campusMapImage.naturalHeight;
  const rect = campusMapImage.getBoundingClientRect();

  const scaleX = naturalWidth / initialDisplayWidth;
  const scaleY = naturalHeight / initialDisplayHeight;

  const x = Math.round((event.clientX - rect.left) * scaleX);
  const y = Math.round((event.clientY - rect.top) * scaleY);

  //クリックされた座標に該当する棟を選択
  for (const campusMapCoordinate of campusMapCoordinates) {
    if (
      x >= campusMapCoordinate[0][0] &&
      y >= campusMapCoordinate[0][1] &&
      x <= campusMapCoordinate[1][0] &&
      y <= campusMapCoordinate[1][1]
    ) {
      for (const wingSwitch of wingSwitches) {
        if (wingSwitch.value == campusMapCoordinate[2]) {
          wingSwitch.checked = true;
          changeWing(wingSwitch.value, wingSwitch);
          break;
        }
      }
      break;
    }
  }
});

//ctrl+enterでチャットボット送信
document
  .getElementById("chatbot-input")
  .addEventListener("keydown", (event) => {
    if (event.ctrlKey && event.key == "Enter") {
      event.preventDefault();
      chatbotSubmit();
    }
  });

//検索の選択肢を初期化
const startWingSelect = document.getElementById("start-wing-select");
const startFloorSelect = document.getElementById("start-floor-select");
const startSectionSelect = document.getElementById("start-section-select");
const goalWingSelect = document.getElementById("goal-wing-select");
const goalFloorSelect = document.getElementById("goal-floor-select");
const goalSectionSelect = document.getElementById("goal-section-select");

//初期化処理
Initializer();

function Initializer() {
  if (is_superuser == true) {
    document.getElementById("notice-management-button").style.display = "";
  }

  //検索の選択肢を初期化
  for (const sectionName of sectionNames) {
    if (sectionName.includes("中継") || sectionName.includes("区画調整")) {
      continue;
    }
    const sectionNameSplits = sectionName.split("_");

    const option = document.createElement("option");
    option.value = sectionName;
    option.dataset.wing = sectionNameSplits[0];
    option.dataset.floor = sectionNameSplits[1];
    option.innerHTML = `${sectionNameSplits[2]}<span class="notranslate"> (</span><span class="wing-name notranslate" data-wing="${sectionNameSplits[0]}">${sectionNameSplits[0]}</span> ${sectionNameSplits[1]})`;
    startSectionSelect.appendChild(option);
  }

  goalWingSelect.innerHTML = startWingSelect.innerHTML;
  goalFloorSelect.innerHTML = startFloorSelect.innerHTML;
  goalSectionSelect.innerHTML = startSectionSelect.innerHTML;

  changeLayoutForResponsive();
  changeFloor(1);
  const inRouteWings = [];

  const wingNames = ["本部棟", "教室棟", "交流棟", "研究棟"];
  if (createdMapFiles) {
    //全体地図の画像を置き換える
    for (const wingName of wingNames) {
      if (createdMapFiles.includes(`${wingName}_whole_map_route.jpg`)) {
        const wholeMapImgElement =
          wholeMapImages[wingName].querySelector("img");
        wholeMapImgElement.src = wholeMapImgElement.src.replace(
          /floor_map\/.*/,
          `floor_map/created_maps/${createdMapFolderName}/${wingName}_whole_map_route.jpg`,
        );
        inRouteWings.push(wingName);
      }
    }
    //選択肢を置き換えてルートに含まれる全体地図を表示する
    for (const wingSwitch of wingSwitches) {
      if (inRouteWings.includes(wingSwitch.value)) {
        wingSwitch.checked = true;
      } else {
        wingSwitch.checked = false;
      }
      changeWing(wingSwitch.value, wingSwitch);
    }
  } else {
    //初期表示を教室棟4階付近にする
    wholeMapImages[currentWing].scrollTop =
      wholeMapImages[currentWing].scrollHeight * 0.39;
  }

  //翻訳
  if (language == "JA") {
    language = "ja";
  }

  if (language != "ja") {
    changeLanguage(language);
    return;
  }

  const cookieLangage = getCookieValue("googtrans");
  if (cookieLangage && cookieLangage.split("/")[2]) {
    changeLanguage(cookieLangage.split("/")[2]);
    return;
  }
}

function getCookieValue(name) {
  const cookies = document.cookie.split("; ");

  for (const cookie of cookies) {
    const [key, ...valueParts] = cookie.split("=");

    if (key === name) {
      return decodeURIComponent(valueParts.join("="));
    }
  }

  return null;
}

window.addEventListener("resize", changeLayoutForResponsive);

function changeLayoutForResponsive() {
  if (window.innerWidth < 800) {
    closeSidebar("index-sidebar", "sidebar-open-button");
  }
}
