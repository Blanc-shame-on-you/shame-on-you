//객체 가져오기
const mainVideo = document.getElementById("mainVideo");
const general = document.getElementById("general");
const GAN = document.getElementById("GAN");
const template = document.getElementById("template");

const firstRow = document.getElementById("firstRow");
const secondRow = document.getElementById("secondRow");
const thirdRow = document.getElementById("thirdRow");

//클릭시 객체의 스타일을 변경
general.onclick = () => {
  mainVideo.style.backgroundImage = "url(./img/black.png)";
};

GAN.onclick = () => {
  mainVideo.style.backgroundImage = "url(./img/icefirebear.png)";
};

template.onclick = () => {
  mainVideo.style.backgroundImage = "url(./img/jangun.png)";
};

//3초뒤 실행
setTimeout(() => {
  firstRow.style.backgroundImage = "url(./img/small_black.png)";
}, 1000);

//6초뒤 실행
setTimeout(() => {
  secondRow.style.backgroundImage = "url(./img/small_icefirebear.png)";
}, 2000);

//9초뒤 실행
setTimeout(() => {
  thirdRow.style.backgroundImage = "url(./img/small_jangun.png)";
}, 3000);
