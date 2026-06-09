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

//チャットボットに質問をする
async function chatbotSubmit() {
  const div = document.querySelector(".chatbot-conversation");
  const chatbotInput = document.querySelector(".chatbot-input");

  //Ajax通信で返答を取得
  const response = await fetch("/chatbot/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
    body: JSON.stringify({
      question: chatbotInput.value,
    }),
  });
  const data = await response.json();

  //ユーザの質問文を描画
  div.insertAdjacentHTML(
    "beforeend",
    `<div class="chatbot-message user-message">${chatbotInput.value}</div>`,
  );

  //テキストボックスをクリア
  chatbotInput.value = "";

  //返答文を描画
  div.insertAdjacentHTML(
    "beforeend",
    `<div class="chatbot-message">${data.chatbot_response}</div>`,
  );
  // console.log(data.chatbot_response);
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
}

//検索をする
function submitSearch() {
  if (!startSectionSelect.value || !goalSectionSelect.value) {
    return;
  }
  location.href = `/search/${encodeURIComponent(startSectionSelect.value)}/${encodeURIComponent(goalSectionSelect.value)}`;
}
//
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

const wholeMapImages = {
  本部棟: document.querySelector('.map-scroll[data-wing="本部棟"]'),
  教室棟: document.querySelector('.map-scroll[data-wing="教室棟"]'),
  交流棟: document.querySelector('.map-scroll[data-wing="交流棟"]'),
  研究棟: document.querySelector('.map-scroll[data-wing="研究棟"]'),
};

const wingFloors = {
  教室棟: ["1", "2", "3", "4", "5", "6", "7"],
  交流棟: ["1", "2", "3", "4", "5"],
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

//表示階を変更
function changeFloor(floorNumber) {
  currentFloorNumber = floorNumber;

  floorMapImage.src = floorMapImage.src.replace(
    /floor_map\/.*/,
    `floor_map/${currentWing}_${floorNumber}階.jpg`,
  );

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
    let firstChecked = true;
    let firstCheckedWing = "";
    for (const wingSwitch of wingSwitches) {
      if (wingSwitch.checked) {
        if (!firstChecked) {
          wingSwitch.checked = false;
        } else {
          firstCheckedWing = wingSwitch.value;
        }
        firstChecked = false;
      }
      wingSwitch.type = "radio";
      floorMapImageArea.style.display = "";
      wholeMapImageArea.style.display = "none";
    }
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
    if (currentWing == wingName) {
      return;
    }

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
    if (inputElement.checked) {
      wholeMapImages[wingName].style.display = "block";
      wholeMapImages[wingName].scrollTop =
        wholeMapImages[wingName].scrollHeight;
    } else {
      wholeMapImages[wingName].style.display = "none";
    }
  }
}

//---------------地図切り替え処理 終了---------------

//html等を書き換える
function changeLanguage(language) {
  console.log(`${language}に切り替えます`);
}

//サーバーから変数を受け取る
const alertMessage = JSON.parse(
  document.getElementById("alert_message").textContent,
);

if (alertMessage) {
  alert(alertMessage);
}

const username = JSON.parse(document.getElementById("username").textContent);

const is_superuser = JSON.parse(
  document.getElementById("is_superuser").textContent,
);

if (is_superuser == true) {
  console.log("管理者でログイン");
}

const language = JSON.parse(document.getElementById("language").textContent);

const sectionNames = JSON.parse(
  document.getElementById("section_names").textContent,
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

//画像クリックで座標を送信
floorMapImage.addEventListener("click", async (event) => {
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

  if (language != "JA") {
    changeLanguage(language);
  }

  for (const sectionName of sectionNames) {
    if (sectionName.includes("中継") || sectionName.includes("区画調整")) {
      continue;
    }
    const sectionNameSplits = sectionName.split("_");

    const option = document.createElement("option");
    option.value = sectionName;
    option.dataset.wing = sectionNameSplits[0];
    option.dataset.floor = sectionNameSplits[1];
    option.textContent = `${sectionNameSplits[2]} （${sectionNameSplits[0]}${sectionNameSplits[1]}）`;
    startSectionSelect.appendChild(option);
  }

  goalWingSelect.innerHTML = startWingSelect.innerHTML;
  goalFloorSelect.innerHTML = startFloorSelect.innerHTML;
  goalSectionSelect.innerHTML = startSectionSelect.innerHTML;

  changeLayoutForResponsive();
  changeFloor(1);
}

window.addEventListener("resize", changeLayoutForResponsive);

function changeLayoutForResponsive() {
  if (window.innerWidth < 800) {
    closeSidebar("index-sidebar", "sidebar-open-button");
  }
}
