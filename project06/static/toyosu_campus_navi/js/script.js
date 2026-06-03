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

//---------------地図切り替え処理 開始---------------

let currentWing = "本部棟";
let currentFloorNumber = 1;
let isFloorMapMode = true;

const wingFloors = {
  教室棟: ["1", "2", "3", "4", "5", "6", "7"],
  交流棟: ["1", "2", "3", "4", "5", "6", "7"],
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
  const floorMapImg = document.getElementById("map-img");

  floorMapImg.src = floorMapImg.src.replace(
    /floor_map\/.*/,
    `floor_map/${currentWing}_${floorNumber}階.jpg`,
  );

  const floorSelectElements = document.querySelectorAll(".floor-select");
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
function toggleDimention(buttonImg) {
  isFloorMapMode = !isFloorMapMode;
  if (isFloorMapMode) {
    buttonImg.src = buttonImg.src.replace(
      /image\/.*/,
      `image/切り替え_平面.png`,
    );
  } else {
    buttonImg.src = buttonImg.src.replace(
      /image\/.*/,
      `image/切り替え_立体.png`,
    );
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
  console.log("aa");
}

const language = JSON.parse(document.getElementById("language").textContent);

//panzoom
const panzoom = Panzoom($("#map-img")[0], {
  maxScale: 5,
  minScale: 0.05,

  contain: null,
});

// ホイールズーム
document
  .querySelector(".viewer")
  .addEventListener("wheel", panzoom.zoomWithWheel);

//初期化処理
Initializer();

function Initializer() {
  if (is_superuser == true) {
    document.getElementById("notice-management-button").style.display = "";
  }

  if (language != "JA") {
    changeLanguage(language);
  }

  changeFloor(1);
}
