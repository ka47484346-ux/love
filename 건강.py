
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>오늘의 건강 길잡이</title>

<style>
:root {
  --green: #397b63;
  --mint: #eaf5ef;
  --cream: #fbfaf6;
  --ink: #24352f;
  --line: #e2e9e4;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: var(--cream);
  color: var(--ink);
  font-family: sans-serif;
  line-height: 1.6;
}

header {
  padding: 40px 20px;
  background: linear-gradient(135deg,#e8f4ed,#f7f5e9);
  text-align: center;
}

h1 {
  font-size: 36px;
  margin: 12px 0;
}

main {
  max-width: 900px;
  margin: 28px auto;
  padding: 0 16px;
}

.panel {
  background: white;
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 22px;
  margin-bottom: 18px;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  border: 1px solid #dce8df;
  background: #f8fbf8;
  color: #385b4a;
  padding: 9px 14px;
  border-radius: 30px;
  cursor: pointer;
}

.chip.active {
  background: var(--mint);
  border-color: var(--green);
  font-weight: bold;
}

textarea, input, select {
  width: 100%;
  padding: 13px;
  border: 1px solid #d5e0d9;
  border-radius: 12px;
  font-size: 15px;
  margin: 8px 0 14px;
}

textarea {
  min-height: 110px;
}

.primary {
  width: 100%;
  background: var(--green);
  color: white;
  border: none;
  padding: 15px;
  border-radius: 13px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
}

.result-grid {
  display: grid;
  grid-template-columns:
    repeat(auto-fit,minmax(220px,1fr));
  gap: 12px;
}

.info {
  background: #f8faf8;
  border: 1px solid var(--line);
  padding: 15px;
  border-radius: 14px;
}

.notice {
  background: #fff1df;
  padding: 14px;
  border-radius: 13px;
  margin-top: 15px;
}

.danger {
  background: #fff0ef;
  padding: 16px;
  border-radius: 15px;
  margin-bottom: 18px;
}

#results {
  display: none;
}
</style>
</head>

<body>

<header>
  <p>MY HEALTH GUIDE</p>
  <h1>오늘의 건강 길잡이</h1>
  <p>증상을 입력하고 건강 관리 방법을 알아봐요.</p>
</header>

<main>

<section class="danger">
  <h3>응급 상황 안내</h3>
  숨쉬기 어렵거나 심한 가슴 통증, 의식 혼란 등
  위급한 증상이 있다면 즉시 119에 연락하세요.
</section>

<section class="panel">

<h2>어떤 증상이 있나요?</h2>
<p>여러 증상을 동시에 선택할 수 있어요.</p>

<div class="chips" id="chips">
  <button class="chip" data-value="기침">기침</button>
  <button class="chip" data-value="콧물">콧물</button>
  <button class="chip" data-value="목 아픔">목 아픔</button>
  <button class="chip" data-value="열">열</button>
  <button class="chip" data-value="두통">두통</button>
  <button class="chip" data-value="복통">복통</button>
  <button class="chip" data-value="속쓰림">속쓰림</button>
  <button class="chip" data-value="설사">설사</button>
  <button class="chip" data-value="변비">변비</button>
  <button class="chip" data-value="재채기">재채기</button>
  <button class="chip" data-value="가려움">가려움</button>
  <button class="chip" data-value="어지러움">어지러움</button>
  <button class="chip" data-value="피로">피로</button>
  <button class="chip" data-value="근육통">근육통</button>
  <button class="chip" data-value="코막힘">코막힘</button>
  <button class="chip" data-value="메스꺼움">메스꺼움</button>
</div>

<p id="selectedCount">선택한 증상 0개</p>
<button class="chip" id="clearSymptoms">선택 초기화</button>

<label>증상 자세히 적기</label>
<textarea id="symptoms"
placeholder="증상에 대한 추가 설명을 입력하세요."></textarea>

<label>언제부터 증상이 있었나요?</label>
<input id="duration"
placeholder="예: 오늘 아침부터">

<label>나이대</label>
<select id="age">
  <option value="">선택하지 않음</option>
  <option>13세 미만</option>
  <option>13~18세</option>
  <option>19~64세</option>
  <option>65세 이상</option>
</select>

<button class="primary" id="analyze">
가능한 원인과 관리 방법 보기
</button>

</section>

<section class="panel" id="results">
<h2>살펴볼 수 있는 가능성</h2>
<p id="intro"></p>
<div class="result-grid" id="cards"></div>

<div class="notice">
<strong>약국 이용 팁</strong><br>
약은 나이, 알레르기, 복용 중인 약에 따라
적합성이 달라질 수 있어요.
약사에게 증상을 설명하고 상담하세요.
</div>
</section>

</main>

<script>

// 증상별 건강정보 데이터
const data = [

{
keys:["기침","콧물","코막힘","재채기","목 아픔"],
title:"감기 등 상기도 감염 가능성",
desc:"바이러스 감염이나 알레르기 등에서 나타날 수 있어요.",
med:"약국에서 증상에 맞는 기침·콧물 완화 일반의약품을 상담하세요.",
good:["물","따뜻한 차","부드러운 국물"],
avoid:["너무 맵거나 뜨거운 음식"],
care:"충분히 쉬고 물을 자주 마시세요."
},

{
keys:["열","두통","몸살","근육통"],
title:"바이러스 감염 등 가능성",
desc:"감기나 독감 등 여러 감염에서 나타날 수 있어요.",
med:"해열·진통제의 연령별 적합성을 약사와 확인하세요.",
good:["물","죽","수프"],
avoid:["과도한 카페인"],
care:"체온과 증상을 관찰하고 충분히 쉬세요."
},

{
keys:["복통","속쓰림","메스꺼움"],
title:"소화불량·위장 자극 가능성",
desc:"식습관이나 위장 자극 등 다양한 원인이 있어요.",
med:"속쓰림 완화제 등은 약사에게 상담하세요.",
good:["미지근한 물","부드러운 음식"],
avoid:["기름진 음식","맵고 자극적인 음식"],
care:"통증이 심하거나 반복 구토가 있으면 진료받으세요."
},

{
keys:["설사","구토"],
title:"장염 등 위장관 문제 가능성",
desc:"바이러스 감염이나 음식으로 인한 문제일 수 있어요.",
med:"경구수분보충액 등을 약사와 상담하세요.",
good:["물","경구수분보충액","죽"],
avoid:["기름진 음식","당이 많은 음료"],
care:"탈수 증상이 나타나면 진료받으세요."
},

{
keys:["변비"],
title:"변비 가능성",
desc:"수분과 식이섬유 섭취 부족 등이 영향을 줄 수 있어요.",
med:"변비약은 연령에 맞게 약사와 상담하세요.",
good:["물","채소","과일"],
avoid:["물을 적게 마시는 습관"],
care:"규칙적인 배변 습관을 유지하세요."
},

{
keys:["재채기","가려움","눈물","맑은 콧물"],
title:"알레르기 비염 가능성",
desc:"알레르기 반응으로 나타날 수 있어요.",
med:"항히스타민제 등을 약사에게 상담하세요.",
good:["물","자극이 적은 음식"],
avoid:["알레르기 유발 물질"],
care:"증상이 지속되면 진료받으세요."
}

];

// 여러 증상 선택 기능
const buttons = document.querySelectorAll(".chip[data-value]");
const textarea = document.getElementById("symptoms");

function updateSymptoms() {
  const selected = [...buttons]
    .filter(b => b.classList.contains("active"))
    .map(b => b.dataset.value);

  textarea.value = [
    ...selected,
    textarea.dataset.extra || ""
  ].filter(Boolean).join(", ");

  document.getElementById("selectedCount").textContent =
    "선택한 증상 " + selected.length + "개";
}

buttons.forEach(button => {
  button.addEventListener("click", () => {
    button.classList.toggle("active");
    updateSymptoms();
  });
});

// 직접 입력한 증상 유지
textarea.addEventListener("input", () => {
  const selected = [...buttons]
    .filter(b => b.classList.contains("active"))
    .map(b => b.dataset.value);

  const typed = textarea.value
    .split(",")
    .map(x => x.trim())
    .filter(Boolean);

  textarea.dataset.extra = typed
    .filter(x => !selected.includes(x))
    .join(", ");
});

// 선택 초기화
document.getElementById("clearSymptoms")
.addEventListener("click", () => {
  buttons.forEach(b => b.classList.remove("active"));
  textarea.value = "";
  textarea.dataset.extra = "";
  document.getElementById("selectedCount").textContent =
    "선택한 증상 0개";
});

// 증상 분석
document.getElementById("analyze")
.addEventListener("click", () => {

  const symptoms = textarea.value.trim();

  if (!symptoms) {
    alert("증상을 하나 이상 선택하거나 입력해주세요.");
    return;
  }

  const matches = data.filter(item =>
    item.keys.some(key => symptoms.includes(key))
  );

  const cards = document.getElementById("cards");
  cards.innerHTML = "";

  document.getElementById("intro").textContent =
    "입력한 증상과 관련될 수 있는 일반 건강정보입니다. " +
    "증상만으로 질환을 확정할 수는 없습니다.";

  const results = matches.length ? matches : [{
    title:"원인을 특정하기 어려워요",
    desc:"입력한 증상만으로 원인을 판단하기 어려워요.",
    med:"약사 또는 의료진과 상담하세요.",
    good:["물","충분한 휴식"],
    avoid:["증상을 악화시키는 음식"],
    care:"증상이 심해지면 진료받으세요."
  }];

  results.forEach(item => {

    const card = document.createElement("article");
    card.className = "info";

    card.innerHTML = `
      <h3>${item.title}</h3>
      <p><b>가능한 원인</b><br>${item.desc}</p>
      <p><b>약국 상담</b><br>${item.med}</p>
      <p><b>도움 되는 음식</b><br>${item.good.join(", ")}</p>
      <p><b>피하면 좋은 것</b><br>${item.avoid.join(", ")}</p>
      <p><b>생활 관리</b><br>${item.care}</p>
    `;

    cards.appendChild(card);
  });

  if(["13세 미만","13~18세"].includes(
    document.getElementById("age").value
  )) {
    document.getElementById("intro").textContent +=
      " 청소년·어린이는 보호자와 함께 약사에게 약의 적합성을 확인하세요.";
  }

  document.getElementById("results").style.display = "block";

  document.getElementById("results")
    .scrollIntoView({behavior:"smooth"});
});

</script>

</body>
</html>
