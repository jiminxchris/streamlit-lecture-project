import streamlit as st

import streamlit.components.v1 as components



st.set_page_config(page_title="모눈종이 최단 경로 시뮬레이터", layout="centered")



st.title("모눈종이 최단 경로 시뮬레이터")



st.write("👣 **좌클릭:** A, B 및 필수 경유지(C, D...) 지정")

st.write("🚫 **우클릭:** 반드시 지나지 않아야 하는 **장애물(O)** 지정")



html_code = """

<!DOCTYPE html>

<html lang="ko">

<head>

<meta charset="UTF-8">

<style>

  body {

    font-family: "Noto Sans KR", sans-serif;

    background: #f6f8fb;

    display: flex;

    flex-direction: column;

    align-items: center;

  }

  .controls { margin-bottom: 10px; display: flex; flex-wrap: wrap; justify-content: center; gap: 10px;}

  button { 

    margin: 5px; 

    padding: 6px 14px; 

    font-size: 14px; 

    cursor: pointer; 

    border: none; 

    border-radius: 8px; 

    background-color: #4a90e2; 

    color: white; 

    white-space: nowrap; 

  }

  button:hover { background-color: #357ab8; }

  #canvas { border: 1px solid #888; background-color: white; margin-bottom: 15px; }

  #result { margin: 8px; font-weight: bold; }

  #examples { 

    display: flex; flex-direction: row; flex-wrap: wrap; gap: 15px; justify-content: center; width: 100%; padding: 10px;

  }

  .path-example { border: 1px solid #ccc; background: #fff; padding: 5px; box-sizing: border-box; }

  .path-info { width: 100%; text-align: center; font-size: 14px; margin-bottom: 10px; }

  .option-group { border: 1px solid #ccc; padding: 5px 10px; border-radius: 5px; background: #fff; display: flex; align-items: center; gap: 10px; }

</style>

</head>

<body>

  <div class="controls">

    <div class="option-group">

        <label for="reuse_yes">

            <input type="radio" id="reuse_yes" name="edge_reuse" value="yes" checked> 

            지나간 경로를 다시 지날 수 있음

        </label>

        <label for="reuse_no">

            <input type="radio" id="reuse_no" name="edge_reuse" value="no"> 

            지나간 경로를 다시 지날 수 없음

        </label>

    </div>
    <button id="init">초기화</button>
    
    <button id="calculate">경우의 수 구하기</button>

    <button id="show">사례 보기</button>

    <button id="grid3">3x3 설정</button>

    <button id="grid4">4x4 설정</button>

    <button id="grid5">5x5 설정</button>

  </div>

  <canvas id="canvas" width="420" height="420"></canvas>

  <div id="result"></div>

  <div id="examples"></div>



<script>

let n = 4;

const canvas = document.getElementById("canvas");

const ctx = canvas.getContext("2d");

let points = {};

let obstacles = {}; 

let clickOrder = []; 

let pathOrder = []; 

let gap = 80;

const MAX_EXAMPLES_TO_DISPLAY = 500; 

const MAX_PATHS_FOR_VISUALIZATION = 100000;



function coordToKey(x, y) { return `${x},${y}`; }

function isObstacle(x, y) { return obstacles[coordToKey(x, y)] !== undefined; }



function updatePathOrder() {

    pathOrder = [];

    if (points.A) pathOrder.push("A");

    for (let i = 2; i < clickOrder.length; i++) {

        pathOrder.push(clickOrder[i]);

    }

    if (points.B) pathOrder.push("B");

}



function drawGrid() {

  ctx.clearRect(0,0,canvas.width,canvas.height);

  ctx.strokeStyle = "#aaa";

  ctx.lineWidth = 1;

  // 모눈선 그리기

  for (let i = 0; i <= n; i++) {

    ctx.beginPath(); ctx.moveTo(40, 40 + i*gap); ctx.lineTo(40 + n*gap, 40 + i*gap); ctx.stroke();

    ctx.beginPath(); ctx.moveTo(40 + i*gap, 40); ctx.lineTo(40 + i*gap, 40 + n*gap); ctx.stroke();

  }

  

  // 장애물(O) 그리기

  for (const key in obstacles) {

      const [x, y] = key.split(',').map(Number);

      ctx.beginPath(); ctx.arc(40 + x*gap, 40 + y*gap, 8, 0, Math.PI*2); ctx.fillStyle = "#2ecc71"; ctx.fill();

      ctx.fillStyle = "white"; ctx.font = "bold 12px sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("O", 40 + x*gap, 40 + y*gap);

  }



  // 필수 지점 (A, B, C...) 그리기

  for (const [key, {x, y}] of Object.entries(points)) {

    ctx.beginPath(); ctx.arc(40 + x*gap, 40 + y*gap, 8, 0, Math.PI*2);

    ctx.fillStyle = key==="A"?"#ff6f61":key==="B"?"#4a90e2":"#f5b041"; ctx.fill();

    ctx.fillStyle = "white"; ctx.font = "bold 12px sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText(key, 40 + x*gap, 40 + y*gap);

  }

}



// (클릭 및 우클릭 이벤트는 동일하게 유지)

canvas.addEventListener("click", (e)=>{

  const rect = canvas.getBoundingClientRect();

  const x = Math.round((e.clientX - rect.left - 40)/gap);

  const y = Math.round((e.clientY - rect.top - 40)/gap);

  if (x < 0 || x > n || y < 0 || y > n) return;

  

  const key = coordToKey(x, y);

  if (isObstacle(x, y)) return; 



  let label;

  if (!points.A) { label = "A"; } else if (!points.B) { label = "B"; } else {

    let i = clickOrder.length;

    label = String.fromCharCode(65 + i); 

    if (i >= 26) return; 

  }



  for(const [k, p] of Object.entries(points)){

      if(p.x === x && p.y === y && k !== label){

          delete points[k];

          clickOrder = clickOrder.filter(item => item !== k);

      }

  }



  points[label] = {x, y};

  if (!clickOrder.includes(label)) { clickOrder.push(label); }

  updatePathOrder();

  drawGrid();

});



canvas.addEventListener("contextmenu", (e)=>{

    e.preventDefault(); 

    const rect = canvas.getBoundingClientRect();

    const x = Math.round((e.clientX - rect.left - 40)/gap);

    const y = Math.round((e.clientY - rect.top - 40)/gap);

    if (x < 0 || x > n || y < 0 || y > n) return;

    

    const key = coordToKey(x, y);



    for(const [k, p] of Object.entries(points)){

        if(p.x === x && p.y === y){ return; } 

    }



    if (isObstacle(x, y)) { delete obstacles[key]; } else { obstacles[key] = {x, y}; }

    

    drawGrid();

});



function comb(n,r){ 

  if (r < 0 || r > n) return 0;

  if (r === 0 || r === n) return 1;

  if (r > n / 2) r = n - r; 



  let res = 1;

  for (let i = 1; i <= r; i++) {

    res = res * (n - i + 1) / i;

  }

  return Math.round(res); 

}



function pathCountWithObstacles(p1, p2, obstacleList){

    const dx = Math.abs(p2.x - p1.x); 

    const dy = Math.abs(p2.y - p1.y); 



    let totalPaths = comb(dx + dy, dx); 



    const relevantObstacles = obstacleList.filter(o => {

        const x_min = Math.min(p1.x, p2.x);

        const x_max = Math.max(p1.x, p2.x);

        const y_min = Math.min(p1.y, p2.y);

        const y_max = Math.max(p1.y, p2.y);

        return o.x >= x_min && o.x <= x_max && o.y >= y_min && o.y <= y_max;

    });

    

    if (relevantObstacles.length === 0) return totalPaths;



    let finalCount = totalPaths;

    

    const startPoint = { x: Math.min(p1.x, p2.x), y: Math.min(p1.y, p2.y) };

    relevantObstacles.sort((a, b) => (Math.abs(a.x - startPoint.x) + Math.abs(a.y - startPoint.y)) - (Math.abs(b.x - startPoint.x) + Math.abs(b.y - startPoint.y)));





    for (let count = 1; count <= relevantObstacles.length; count++) {

        let combinationSum = 0;

        const indices = new Array(count).fill(0).map((_, i) => i);



        let done = false;

        while (!done) {

            const currentObstacles = indices.map(i => relevantObstacles[i]);

            let pathProduct = 1;

            const pointsToCalculate = [p1, ...currentObstacles, p2];



            for (let i = 0; i < pointsToCalculate.length - 1; i++) {

                const start = pointsToCalculate[i];

                const end = pointsToCalculate[i+1];

                const segmentDx = Math.abs(end.x - start.x);

                const segmentDy = Math.abs(end.y - start.y);

                pathProduct *= comb(segmentDx + segmentDy, segmentDx);

            }

            

            combinationSum += pathProduct;



            let k = indices.length - 1;

            while (k >= 0 && indices[k] === relevantObstacles.length - count + k) { k--; }

            if (k < 0) {

                done = true;

            } else {

                indices[k]++;

                for (let j = k + 1; j < indices.length; j++) {

                    indices[j] = indices[j - 1] + 1;

                }

            }

        } 

        if (count % 2 === 1) { finalCount -= combinationSum; } else { finalCount += combinationSum; }

    }

    

    return finalCount < 0 ? 0 : finalCount; 

}





// **[핵심 함수]** 다단계 경로 계산 (선택지에 따라 분기)

function calculateTotalPaths(allowEdgeReuse){

    if(pathOrder.length < 2) return 0;

    

    let total = 1;

    let pathPossible = true;



    if (allowEdgeReuse) {

        // **1. 간선 재사용 허용 (단순 곱셈)**

        for(let i=0;i<pathOrder.length-1;i++){

            const p1 = points[pathOrder[i]];

            const p2 = points[pathOrder[i+1]];

            

            // L 이동이 필요한 구간은 최단 경로로 정의할 수 없어 제외

            if (p2.x < p1.x && p2.y > p1.y) { 

                pathPossible = false; total = 0; break;

            }



            const count = pathCountWithObstacles(p1, p2, Object.values(obstacles));



            if (count === 0) {

                pathPossible = false;

                total = 0;

                break;

            }

            total *= count;

        }

        return total;



    } else {

        // **2. 간선 재사용 불가능 (Simple Path, 간선 중복 제거)**

        

        // 경유지 1개 (A -> C -> B)인 경우에만 간선 중복 제거 로직 적용

        if (pathOrder.length === 3) {

            const A = points[pathOrder[0]];

            const C = points[pathOrder[1]];

            const B = points[pathOrder[2]];



            if (C.x < A.x || C.y > n || C.y < 0 || B.x < C.x || B.y > n || B.y < 0) return 0;

            if (B.x < A.x && B.y > A.y) return 0; 



            let validTotal = 0;



            // 1. A->(C.x-1, C.y) [R 도착] * C->B 경로 중 L 시작 제외 (C->B는 최단 경로이므로 L 시작은 없음)

            const CL = {x: C.x - 1, y: C.y};

            if (C.x > 0 && !isObstacle(CL.x, CL.y) && CL.x >= A.x && CL.y >= Math.min(A.y, C.y) && CL.y <= Math.max(A.y, C.y)) {

                const count_A_CL = pathCountWithObstacles(A, CL, Object.values(obstacles));

                validTotal += count_A_CL * pathCountWithObstacles(C, B, Object.values(obstacles));

            }



            // 2. A->(C.x, C.y-1) [D 도착] * C->B 경로 중 U 시작 제외

            const CU = {x: C.x, y: C.y - 1};

            if (C.y > 0 && !isObstacle(CU.x, CU.y) && CU.y >= Math.min(A.y, C.y) && CU.x >= Math.min(A.x, C.x) && CU.x <= Math.max(A.x, C.x)) {

                const count_A_CU = pathCountWithObstacles(A, CU, Object.values(obstacles));

                if (C.y > B.y) {

                    const paths_C_U_B = pathCountWithObstacles(CU, B, Object.values(obstacles));

                    validTotal += count_A_CU * (pathCountWithObstacles(C, B, Object.values(obstacles)) - paths_C_U_B);

                } else { 

                    validTotal += count_A_CU * pathCountWithObstacles(C, B, Object.values(obstacles));

                }

            }



            // 3. A->(C.x, C.y+1) [U 도착] * C->B 경로 중 D 시작 제외

            const CD = {x: C.x, y: C.y + 1};

            if (C.y < n && !isObstacle(CD.x, CD.y) && CD.y <= Math.max(A.y, C.y) && CD.x >= Math.min(A.x, C.x) && CD.x <= Math.max(A.x, C.x)) {

                const count_A_CD = pathCountWithObstacles(A, CD, Object.values(obstacles));

                if (C.y < B.y) {

                    const paths_C_D_B = pathCountWithObstacles(CD, B, Object.values(obstacles));

                    validTotal += count_A_CD * (pathCountWithObstacles(C, B, Object.values(obstacles)) - paths_C_D_B);

                } else { 

                    validTotal += count_A_CD * pathCountWithObstacles(C, B, Object.values(obstacles));

                }

            }



            return validTotal;

            

        } else {

             // 경유지가 2개 이상일 경우, 간선 중복 제거가 조합 공식으로 불가능하여 단순 곱셈으로 대체합니다.
             // (Simple Path) 텍스트 제거 
             document.getElementById("result").textContent=`경유지가 2개 이상일 경우, 계산이 복잡하여 시각화 결과 기반으로만 판단해야 합니다.`;

             for(let i=0;i<pathOrder.length-1;i++){

                const p1 = points[pathOrder[i]];

                const p2 = points[pathOrder[i+1]];

                if (p2.x < p1.x && p2.y > p1.y) return 0;

                const count = pathCountWithObstacles(p1, p2, Object.values(obstacles));

                if (count === 0) return 0;

                total *= count;

            }

            return total;

        }

    }

}





document.getElementById("calculate").addEventListener("click", ()=>{

  const allowEdgeReuse = document.getElementById('reuse_yes').checked;

  const total = calculateTotalPaths(allowEdgeReuse);


  // 사용자 요청: '(Simple Path)' 제거
  const modeText = allowEdgeReuse ? "간선 재사용 허용" : "간선 재사용 불가";


  if (total === 0) {

      document.getElementById("result").textContent=`[${modeText}] 총 최단거리 경로 수: 0 가지 (경로 불가)`;

  } else if (total > 1000000) { 

      document.getElementById("result").textContent=`[${modeText}] 총 최단거리 경로 수: ${total} 가지 (계산됨, 시각화는 제한)`;

  } else {

      document.getElementById("result").textContent=`[${modeText}] 총 최단거리 경로 수: ${total} 가지`;

  }

});





// **사례 보기 함수** (선택지에 따라 간선 중복 체크 로직 분기)

function generatePaths(allowEdgeReuse){

  const allPaths = [];

  let currentTotalPaths = 1;

  

  for(let i=0;i<pathOrder.length-1;i++){

    const p1 = points[pathOrder[i]];

    const p2 = points[pathOrder[i+1]];

    const segmentPaths = [];



    if (p2.x < p1.x && p2.y > p1.y) { return []; } 



    const requiredLength = Math.abs(p2.x - p1.x) + Math.abs(p2.y - p1.y);



    function dfs(x,y,path){

      if (currentTotalPaths > MAX_PATHS_FOR_VISUALIZATION) return; 

      if (isObstacle(x, y)) return; 

      if (path.length > requiredLength) return; 

      
      if(x===p2.x && y===p2.y){ 

        if (path.length === requiredLength) { 

             segmentPaths.push([...path]);

        }

        return; 

      }

      
      const directions = [];

      if(x<p2.x) directions.push({dx: 1, dy: 0, dir: "R"}); 

      if(p2.y >= p1.y && y<p2.y) directions.push({dx: 0, dy: 1, dir: "D"}); 

      if(p2.y < p1.y && y>p2.y) directions.push({dx: 0, dy: -1, dir: "U"}); 

      
      for(const {dx, dy, dir} of directions){

          dfs(x + dx, y + dy, [...path, dir]);

      }

    }

    
    if (isObstacle(p1.x, p1.y)) return []; 

    
    dfs(p1.x,p1.y,[]);

    allPaths.push(segmentPaths);

    
    currentTotalPaths *= segmentPaths.length;

    if (currentTotalPaths > MAX_PATHS_FOR_VISUALIZATION) break;

  }



  if (allPaths.length === 0) return [];

  
  let finalPaths = allPaths[0].map(p => ({path: p, edges: new Set()}));

  
  // 첫 번째 구간의 간선 설정

  finalPaths.forEach(item => {

      let currentX = points[pathOrder[0]].x;

      let currentY = points[pathOrder[0]].y;

      item.path.forEach(step => {

          const nextX = currentX + (step === "R" ? 1 : 0);

          const nextY = currentY + (step === "D" ? 1 : step === "U" ? -1 : 0);

          const key = coordToKey(currentX, currentY) + '->' + coordToKey(nextX, nextY);

          item.edges.add(key);

          currentX = nextX;

          currentY = nextY;

      });

  });



  // 두 번째 구간부터 간선 중복 체크 (allowEdgeReuse == false일 때만)

  for (let i = 1; i < allPaths.length; i++) {

    const nextSegmentPaths = allPaths[i];

    const segmentStartPoint = points[pathOrder[i]];

    const newFinalPaths = [];

    
    for (const item of finalPaths) {

      for (const nextPath of nextSegmentPaths) {

        if (newFinalPaths.length >= MAX_EXAMPLES_TO_DISPLAY) break;

        
        let isSimplePath = true;

        const newEdges = new Set(item.edges);

        let currentX = segmentStartPoint.x;

        let currentY = segmentStartPoint.y;


        for (const step of nextPath) {

             const nextX = currentX + (step === "R" ? 1 : 0);

             const nextY = currentY + (step === "D" ? 1 : step === "U" ? -1 : 0);

             
             const key = coordToKey(currentX, currentY) + '->' + coordToKey(nextX, nextY);

             const reverseKey = coordToKey(nextX, nextY) + '->' + coordToKey(currentX, currentY);


             // **[핵심 분기]** 간선 재사용 불가능 모드일 때만 체크

             if (!allowEdgeReuse && (item.edges.has(key) || item.edges.has(reverseKey))) {

                 isSimplePath = false;

                 break;

             }

             
             newEdges.add(key);

             currentX = nextX;

             currentY = nextY;

        }


        if (allowEdgeReuse || isSimplePath) { // 재사용 허용이면 isSimplePath 무시

          newFinalPaths.push({

              path: [...item.path, ...nextPath],

              edges: newEdges 

          });

        }

      }

      if (newFinalPaths.length >= MAX_EXAMPLES_TO_DISPLAY) break;

    }

    finalPaths = newFinalPaths;

    if (finalPaths.length === 0) return [];

  }


  return finalPaths.map(item => item.path);

}


document.getElementById("show").addEventListener("click", ()=>{

  const allowEdgeReuse = document.getElementById('reuse_yes').checked;

  const exDiv=document.getElementById("examples");

  exDiv.innerHTML="";

  

  if(pathOrder.length < 2){ exDiv.textContent="최소 두 지점(A와 B)을 먼저 지정하세요."; return; }

  

  const paths=generatePaths(allowEdgeReuse);

  const totalPathsCount = paths.length;

  const numToDisplay = Math.min(totalPathsCount, MAX_EXAMPLES_TO_DISPLAY);


  const resultText = document.getElementById("result").textContent;

  let pathCalcTotal = 0;

  const match = resultText.match(/:\s*(\d+)/);

  if (match) pathCalcTotal = parseInt(match[1]);


  const infoDiv=document.createElement("div");

  infoDiv.className="path-info";

  
  if (totalPathsCount === 0) {

      infoDiv.textContent = "조건을 만족하는 최단 경로가 없습니다.";

      exDiv.appendChild(infoDiv);

      return;

  }

  
  // 사용자 요청: 문구를 '총 X가지'로 단순화하고 (Simple Path) 텍스트를 제거
  
  infoDiv.textContent=`총 ${totalPathsCount}가지`;
  
  if (numToDisplay < totalPathsCount) {
     infoDiv.textContent += ` (사례 ${numToDisplay}가지 표시됨)`;
  }
  
  // 수정된 부분 끝


  exDiv.appendChild(infoDiv);


  // 시각화 로직 (생략)

  const allX = pathOrder.map(key => points[key].x);

  const allY = pathOrder.map(key => points[key].y);

  const minX = Math.min(...allX);

  const minY = Math.min(...allY);

  const maxX = Math.max(...allX);

  const maxY = Math.max(...allY);



  const totalDx = maxX - minX;

  const totalDy = maxY - minY;



  const scale=25; 

  const maxMiniSize = 250; 

  const canvasWidth = 10 + totalDx * scale + 10;

  const canvasHeight = 10 + totalDy * scale + 10;

  let skippedCount = 0;





  paths.slice(0, numToDisplay).forEach((path,i)=>{

    const mini=document.createElement("canvas");

    
    if (canvasWidth > maxMiniSize || canvasHeight > maxMiniSize) { skippedCount++; return; }

    mini.width = canvasWidth; mini.height = canvasHeight;

    const c=mini.getContext("2d");

    
    c.strokeStyle="#eee"; c.lineWidth = 1;

    for(let j=0;j<=totalDy;j++){ c.beginPath(); c.moveTo(10,10+j*scale); c.lineTo(10+totalDx*scale,10+j*scale); c.stroke(); }

    for(let j=0;j<=totalDx;j++){ c.beginPath(); c.moveTo(10+j*scale,10); c.lineTo(10+j*scale,10+totalDy*scale); c.stroke(); }

    
    let cx = 10 + (points.A.x - minX) * scale;

    let cy = 10 + (points.A.y - minY) * scale;

    c.beginPath(); c.moveTo(cx,cy);

    path.forEach(step=>{

      if(step==="R") cx+=scale; else if(step==="D") cy+=scale; else if(step==="U") cy-=scale;

      c.lineTo(cx,cy); 

    });

    c.strokeStyle="#ff6f61"; c.lineWidth=2; c.stroke();

    
    pathOrder.forEach(key => {

        const p = points[key];

        const markerX = 10 + (p.x - minX) * scale;

        const markerY = 10 + (p.y - minY) * scale;

        let color = key==="A"?"#ff6f61":key==="B"?"#4a90e2":"#f5b041";

        c.fillStyle = color; c.beginPath(); c.arc(markerX, markerY, 4, 0, Math.PI*2); c.fill();

        c.fillStyle = "white"; c.font = "bold 8px sans-serif"; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText(key, markerX, markerY);

    });

    
    for (const key in obstacles) {

        const obs = obstacles[key];

        const obsX = 10 + (obs.x - minX) * scale;

        const obsY = 10 + (obs.y - minY) * scale;

        c.fillStyle = "#2ecc71"; c.beginPath(); c.arc(obsX, obsY, 4, 0, Math.PI*2); c.fill();

        c.fillStyle = "white"; c.font = "bold 8px sans-serif"; c.textAlign = "center"; c.textBaseline = "middle"; c.fillText("O", obsX, obsY);

    }


    const div=document.createElement("div");

    div.className="path-example";

    div.appendChild(mini);

    exDiv.appendChild(div);

  });

  
  if (skippedCount > 0) {

     exDiv.innerHTML += `<p style='width: 100%; text-align: center;'>* 모눈 크기(${totalDx}x${totalDy})가 너무 커서 ${skippedCount}개 사례의 시각화가 생략되었습니다. *</p>`;

  }

});


document.getElementById("init").addEventListener("click", ()=>{

  points={}; clickOrder=[]; pathOrder=[]; obstacles={};

  document.getElementById("result").textContent="";

  document.getElementById("examples").innerHTML="";

  document.getElementById('reuse_yes').checked = true; // 기본값 유지

  drawGrid();

});


document.getElementById("grid3").addEventListener("click", ()=>{ n=3; gap=100; resizeCanvas(); });

document.getElementById("grid4").addEventListener("click", ()=>{ n=4; gap=80; resizeCanvas(); });

document.getElementById("grid5").addEventListener("click", ()=>{ n=5; gap=60; resizeCanvas(); });



function resizeCanvas(){

  canvas.width = 40 + n*gap + 40;

  canvas.height = 40 + n*gap + 40;

  points={}; clickOrder=[]; pathOrder=[]; obstacles={};

  document.getElementById("result").textContent="";

  document.getElementById("examples").innerHTML="";

  document.getElementById('reuse_yes').checked = true;

  drawGrid();

}


drawGrid();

</script>

</body>

</html>
"""



components.html(html_code, height=12000)