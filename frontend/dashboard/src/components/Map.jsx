import React, { Component } from 'react';
import ward from "./patient_ward.png";

export default class Map extends Component {
    //functions go here
    onImageLoad = () => {
        let canvas = document.getElementById("canvas")
        let context = canvas.getContext('2d')
        context.drawImage(this, 0, 0)
    }

  render() {
    return (
        <div id="parent" class="canvas_parent_div">
            <img src={ward} alt="map" onLoad={this.onImageLoad}></img>
            <canvas id="canvas"></canvas>
        </div>
        
        );
  }
}
