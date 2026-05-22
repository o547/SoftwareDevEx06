//モーダルを活性にする
function openModal() {
  document.getElementById("modal").classList.add("active");
}

//モーダルを非活性にする
function closeModal() {
  document.getElementById("modal").classList.remove("active");
}

//第一引数のメニューを非表示にして、第二引数のメニューを表示する
function toggleMenu(currentMenuId, targetMenuId, displayMethod) {
  document.getElementById(currentMenuId).style.display = "none";
  document.getElementById(targetMenuId).style.display = displayMethod;
}

//サイドバーを閉じる
function closeSidebar(sidebarId,buttonId) {
  const sidebar=document.getElementById(sidebarId);
  const openButton=document.getElementById(buttonId);
  sidebar.classList.add("closed");
  sidebar.style.width = "0";
  openButton.classList.add("active");
}

//サイドバーを開く
function openSidebar(sidebarId,buttonId) {
  const sidebar=document.getElementById(sidebarId);
  const openButton=document.getElementById(buttonId);
  sidebar.classList.remove("closed");
  sidebar.style.width = "300px";
  openButton.style.width = "0";
  openButton.classList.remove("active");
}

//チャットボットに質問をする
async function chatbotSubmit(){

  const div = document.querySelector(".chatbot-conversation");
  const chatbotInput = document.querySelector(".chatbot-input");
  
  //Ajax通信で返答を取得
  const response = await fetch("/chatbot/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
    },
    body: JSON.stringify({
      question: chatbotInput.value
    })
  });
  const data = await response.json();
  
  //ユーザの質問文を描画
  div.insertAdjacentHTML("beforeend", `<div class="chatbot-message user-message">${chatbotInput.value}</div>`);
  
  //テキストボックスをクリア
  chatbotInput.value= "";
  
  //返答文を描画
  div.insertAdjacentHTML("beforeend", `<div class="chatbot-message">${data.chatbot_response}</div>`);
  // console.log(data.chatbot_response);
}

//サーバーから変数を受け取る
const alert_message = JSON.parse(
  document.getElementById("alert_message").textContent
);

if(alert_message){
  alert(alert_message);
}