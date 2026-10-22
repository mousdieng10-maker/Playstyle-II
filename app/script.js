import {find, findAll} from "./call.js";
import {hide, show} from "./utils.js";









// Cache the game screens and controls used by the event handlers below.
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
const marketBackBtn = find("#marketBackBtn");
const commitBuyBtn = find('#commitBuyBtn');
const filterPosition = find('#filterPosition');
const textualFilter = find("#textual-filter");
const soldScreen = find("#soldScreen")
function setText(selector, text){
    for(const element of findAll(selector)){
        element.textContent = text;
    }
}



let incr; 
// Start with only the home screen visible.
hide(generateScreen);
hide(playingScreen);
hide(transfermarket);






// Ask Python for the starting lineup, then populate the pitch and show the game.
enterButton.onclick = async function(){
    hide(homeScreen);
    document.body.className = "background-do";

    show(generateScreen);
    await window.pywebview.api.reload_classes();
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








// Return from the transfer market to the current lineup.
backButton.onclick = async function(){
    // I need to make sure to come back here and add an initializing bridge between the js and python 
    // otherwise the starting eleven will not be updated.
    hide(transfermarket);
    show(playingScreen)
}







// Build a transfer-market card with a player's details and stats from Python.
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

        // Selecting a player opens the buy/sell comparison and commit flow.
        playerDiv.onclick = async function(){
                options.className = "options-show";
                const reciprocate = await window.pywebview.api.selling(player); 
                    setText(".incoming-name", player.name);
                    setText(".incoming-ovr", player.ovr);
                    setText(".incoming-pace", `PAC: ${statList.pace}`);
                    setText(".incoming-dribbling", `DRI: ${statList.dribbling}`);
                    setText(".incoming-defending", `DEF: ${statList.defending}`);
                    setText(".incoming-passing", `PAS: ${statList.passing}`);
                    setText(".incoming-shooting", `SHO: ${statList.shooting}`);
                    setText(".incoming-physical", `PHY: ${statList.physical}`);
                    setText(".incoming-market", `Market Value: ${player.value}`);

                    setText(".outgoing-name", reciprocate.name);
                    setText(".outgoing-ovr", reciprocate.ovr);
                    setText(".outgoing-pace", `PAC: ${reciprocate.pace}`);
                    setText(".outgoing-dribbling", `DRI: ${reciprocate.dribbling}`);
                    setText(".outgoing-defending", `DEF: ${reciprocate.defending}`);
                    setText(".outgoing-passing", `PAS: ${reciprocate.passing}`);
                    setText(".outgoing-shooting", `SHO: ${reciprocate.shooting}`);
                    setText(".outgoing-physical", `PHY: ${reciprocate.physical}`);
                    setText(".outgoing-market", `Market Value: ${reciprocate.value}`);  
                show(options)
                buyBtn.onclick = async function(){
                    hide(options)
                    // Python determines which squad player would be exchanged.
                    
                    let findBudget = await window.pywebview.api.find_budget(); 

                    // Flag the purchase when the available budget is insufficient.
                    if(findBudget < player.value){
                        commitBuyBtn.className = "not-possible";
                        commitBuyBtn.textContent = "too expensive!";
                    }
                    show(marketSell); 
                    marketBackBtn.onclick = function(){
                        commitBuyBtn.className = "opt-btn";
                        commitBuyBtn.textContent = "Commit Buy";
                        hide(marketSell)
                    }
                    commitBuyBtn.onclick = async function(){
                        await window.pywebview.api.sell_player(player, reciprocate)
                        hide(marketSell);
                        hide(transfermarket);
                         // Refresh the pitch after Python updates the squad.
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
                        await window.pywebview.api.transaction(player.value)
                        await window.pywebview.api.reload_classes();
                        show(playingScreen);
                        soldScreen.className = 'sold-true'; 
                        setTimeout(() => {
                            soldScreen.className = 'sold-screen';
                        },2000);

                    }
                    
                }
                bBtn.onclick = function(){
                    hide(options);
                    
                }
                negoBtn.onclick = async function(){

                }

        }
       
        

}







// Load the available players and budget before showing the transfer market.
transferBtn.onclick = async function(){
    incr = 0;
    hide(playingScreen);
    show(generateScreen);
    hide(marketSell);
    document.body.style.display = "flex"; 
    const playerDatabase = await window.pywebview.api.show_all_players();
    await window.pywebview.api.reload_classes();
    for(const player of playerDatabase){
        renderPlayer(player)
    }
    let amount = await window.pywebview.api.return_budget();
    money.textContent = `Current Budget: $${amount}`
    hide(generateScreen);

    show(transfermarket);
}






// Replace the current results with players matching the search query.
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





// List the positions supported by the generated squad and player database.
filterPosition.onclick = async function(){
    transferDiv.innerHTML = ""
    let spinner = document.createElement("div"); 
    spinner.className = "loader"; 
    transferDiv.appendChild(spinner);
    const positionList = ["GK", "CB", "LB", "RB", "CM", "CAM", "LM", "RM", "LW", "RW", "ST","all positions"];
    let selectedPosition = positionList[incr];
    textualFilter.textContent = selectedPosition;
    const relatedPositions = await window.pywebview.api.find_position(selectedPosition); 
    transferDiv.innerHTML = "";
    if(relatedPositions.length > 0){
        for(const result of relatedPositions){
            renderPlayer(result);
        }
    }
    else{
        transferDiv.innerHTML = "No results found";
    }
    
    incr += 1;
    if(incr == positionList.length){
        incr = 0;
    }
    
}
