import {find, findAll} from "./call.js";
import {hide, show} from "./utils.js";
const enterButton = find("#enterBtn");
const homeScreen = find("#homeScreen");
const leftSection = find(".left-section");
const generateScreen = find("#generateScreen");
const playingScreen = find("#playingScreen");

const transferDiv = find("#transferDiv")
const transferBtn = find("#transferBtn");
const transfermarket = find("#transfermarket");
const money = find("#money");
const team = find("#team");
const avgOvr = find("#avgOvr");
const searchPlayer = find(".search-bar"); 
const backButton = find("#backButton");
const options = find("#options");
const buyBtn = find('#buyBtn');
const negoBtn = find('#negoBtn');
const bBtn = find('#bBtn');
const marketSell = find("#marketSell");
hide(generateScreen);
hide(playingScreen);
hide(transfermarket);

enterButton.onclick = async function(){
    hide(homeScreen);
    document.body.className = "background-do";
    show(generateScreen);
    const team = await window.pywebview.api.define_cards();
    for(const player of team){
        const playerName = find(`#${player.position}`);
        const playerCard = playerName.parentElement;
        const positionLabel = playerCard.querySelector(".position-label");
        const playerOVR = playerCard.querySelector(".player-ovr");
        let playerImg = document.createElement("img");

        playerName.textContent = player.name;
        positionLabel.textContent = player.position;
        playerCard.style.backgroundImage = `url(${player.link})`;
        playerOVR.textContent = `${player.ovr}`;
        
    }
    document.body.style.display = "block"; 
    hide(generateScreen);
    show(playingScreen);
}


backButton.onclick = async function(){
    // I need to make sure to come back here and add an initializing bridge between the js and python 
    // otherwise the starting eleven will not be updated.
    hide(transfermarket);
    show(playingScreen)
}
async function renderPlayer(player){
    let playerDiv  = document.createElement("div");
        let playerNameDiv = document.createElement("h2");
        let playerPosDiv = document.createElement("h2");
        let playerOVRDiv = document.createElement("h1");
        let playerValueDiv = document.createElement("h3");
        let priorityInfo = document.createElement("span");
        
        let statList = await window.pywebview.api.give_player_stats(player);   
        let playerPace = document.createElement("h3");
        playerPace.className = "stat";
        playerPace.textContent =   `PAC: ${statList.pace}`
        let playerDribbling = document.createElement("h3");
        playerDribbling.className = "stat";
        playerDribbling.textContent = `DRI: ${statList.dribbling}`
        let playerDefending = document.createElement("h3");
        playerDefending.className = "stat";
        playerDefending.textContent  = `DEF: ${statList.defending}`
        let playerPhysical = document.createElement("h3");
        playerPhysical.className = "stat";
        playerPhysical.textContent = `PHY: ${statList.physical}`
        let playerPassing = document.createElement("h3");
        playerPassing.className = "stat";
        playerPassing.textContent = `PAS: ${statList.passing}`
        let playerShooting = document.createElement("h3");
        playerShooting.className = "stat";
        playerShooting.textContent = `SHO: ${statList.shooting}`
        playerNameDiv.textContent = player.name;
        playerPosDiv.textContent = player.position
        playerOVRDiv.textContent = player.ovr;
        playerValueDiv.textContent = `Market Value: ${player.value}`;
        let leftSection = document.createElement("div");
        let rightSection = document.createElement("div");
        let statSection = document.createElement("span");
        leftSection.className = "temp-profile";
        let playerImg = document.createElement("img"); 
        playerImg.src = `assets/silouhette.webp`;
        playerImg.className = 'profile'
        rightSection.className = "org-info"; 
        leftSection.appendChild(playerImg); 
        priorityInfo.style.display = "flex";
        priorityInfo.style.gap = ".5em"; 
        statSection.style.display = "flex";
        statSection.style.gap = ".3em";
        priorityInfo.style.alignItems = "center";
        priorityInfo.appendChild(playerNameDiv);
        priorityInfo.appendChild(playerOVRDiv);
        rightSection.appendChild(priorityInfo); 
        statSection.appendChild(playerPace);
        statSection.appendChild(playerDribbling);
        statSection.appendChild(playerDefending);
        statSection.appendChild(playerPassing);
        statSection.appendChild(playerShooting);
        statSection.appendChild(playerPhysical);
        rightSection.appendChild(statSection);
        rightSection.appendChild(playerValueDiv);
        playerDiv.className = "transfer-div"; 
        playerDiv.appendChild(leftSection);
        if(player.ovr >= 80){
            playerDiv.classList.add("platinum");
        }
        playerDiv.appendChild(rightSection);
        transferDiv.appendChild(playerDiv);
        playerDiv.onclick = async function(){
            options.className = "options-show";
            show(options)
            buyBtn.onclick = async function(){
                hide(options)
                let reciprocate = window.pywebview.api.selling(player); 
                show(marketSell); 
            }
            bBtn.onclick = function(){
                hide(options);
            }
            negoBtn.onclick = async function(){

            }

        }

}
transferBtn.onclick = async function(){
    hide(playingScreen);
    show(generateScreen);
    document.body.style.display = "flex"; 
    const playerDatabase = await window.pywebview.api.show_all_players();
    
    for(const player of playerDatabase){
        renderPlayer(player)
    }
    money.textContent = await window.pywebview.api.return_budget();
    hide(generateScreen);

    show(transfermarket);
}

searchPlayer.addEventListener("input",async ()=> {
    transferDiv.innerHTML = ""
    let spinner = document.createElement("div");
    spinner.className = "loader"; 
    transferDiv.appendChild(spinner); 
    let results = await window.pywebview.api.find(searchPlayer.value)
    transferDiv.innerHTML = ""
    for(const result of results){
        renderPlayer(result); 
    }
})
