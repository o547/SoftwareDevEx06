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