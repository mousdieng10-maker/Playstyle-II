import {find, findAll} from "./call.js";
import {hide, show} from "./utils.js";
const enterButton = find("#enterBtn");
const homeScreen = find("#homeScreen");
const leftSection = find(".left-section");
const generateScreen = find("#generateScreen");
const playingScreen = find("#playingScreen");


hide(generateScreen);

enterButton.onclick = async function(){
    hide(homeScreen);
    show(generateScreen);
    const team = await window.pywebview.api.generateTeam();
    document.body.style.display = "block"; 
    hide(generateScreen);
    show(playingScreen);
}