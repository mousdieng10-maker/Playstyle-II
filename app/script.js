import {find, findAll} from "./call.js";
import {hide, show} from "./utils.js";
const enterButton = find("#enterBtn");
const homeScreen = find("#homeScreen");
const leftSection = find(".left-section");
const generateScreen = find("#generateScreen");
const playingScreen = find("#playingScreen");

const LW= find("#LW");
const CAM= find("#CAM");
const RW= find("#RW");
const LM= find("#LM");
const CM= find("#CM");
const RM= find("#RM");
const ST= find("#ST");
const LB= find("#LB");
const CB= find("#CB");
const RB= find("#RB");
const GK= find("#GK");
const transferDiv = find("#transferDiv")
const transferBtn = find("#transferBtn");
const transfermarket = find("#transfermarket");
const money = find("#money");
const team = find("#team");
const avgOvr = find("#avgOvr");
const searchPlayer = find(".search-bar"); 

hide(generateScreen);
hide(playingScreen);
hide(transfermarket);

enterButton.onclick = async function(){
    hide(homeScreen);
    show(generateScreen);
    const team = await window.pywebview.api.generate_team();
    for(const player of team){
        let position = player.position;
        if(position == "LW"){
            LW.innerHTML = player.name;

        }
        else if(position == "CAM"){
            CAM.textContent = player.name;
        }
        else if(position == "RW"){
            RW.textContent = player.name;
        }
        else if(position == "LM"){
            LM.textContent = player.name;
        }
        else if(position == "CM"){
            CM.textContent = player.name;
        }
        else if(position == "RM"){
            RM  .textContent = player.name;
        }
        else if(position == "ST"){
            ST.textContent = player.name;
        }
        else if(position == "LB"){
            LB.textContent = player.name;
        }
        else if(position == "CB"){
            CB.textContent = player.name;
        }
        else if(position == "RB"){
            RB.textContent = player.name;
        }
        else if(position == "GK"){
            GK.textContent = player.name;
        }
    }
    document.body.style.display = "block"; 
    hide(generateScreen);
    show(playingScreen);
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
        rightSection.className = "org-info"; 
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
        playerValueDiv.style.color = "purple"; 
        rightSection.appendChild(playerValueDiv);
        playerDiv.className = "transfer-div"; 
        playerDiv.appendChild(leftSection);
        if(player.ovr >= 80){
            playerDiv.style.color = "white"; 
            playerDiv.classList.add("platinum");
            playerValueDiv.style.color = "gold"; 
        }
        playerDiv.appendChild(rightSection);
        transferDiv.appendChild(playerDiv);


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

