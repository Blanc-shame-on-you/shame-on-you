//객체 가져오기
const mainVideo = document.getElementById("mainVideo");
const general = document.getElementById("general");
const GAN = document.getElementById("GAN");
const template = document.getElementById("template");

var first_img = document.getElementById("firstImage");
var second_img = document.getElementById("secondImage");
var third_img = document.getElementById("thirdImage");
var fourth_img = document.getElementById("fourthImage");
var fifth_img = document.getElementById("fifthImage");

var bottom_imgs = [first_img, second_img, third_img, fourth_img, fifth_img](
  //클릭시 객체의 스타일을 변경
  (general.onclick = () => {
    mainVideo.src = "{{ url_for('video_feed', tag_id='general') }}";
  })
);

GAN.onclick = () => {
  mainVideo.src = "{{ url_for('video_feed', tag_id='GAN') }}";
};

template.onclick = () => {
  mainVideo.src = "{{ url_for('video_feed', tag_id='template') }}";
};

//1초에 한 번씩 초기화
setInterval(() => {
  fetch("http://10.120.72.244:5000/getData").then((res) => {
    res_json = res.json()["data"];
    for (var i = 0; i < res_json.length; i++) {
      bottom_imgs[i].src = res_json[i]["img"];
    }
  });
}, 1000);
