import React, { Component } from 'react';
import ward from "./patient_ward.png" 

export default class Map extends Component {
  
  patient_locs = [[150, 50], [50, 130], [52, 375], [150, 475], [360, 475]]

  onLoadImg = () => {
    let img = document.getElementById("ward")
    let canvas = document.getElementById("canvas")
    let ctx = canvas.getContext('2d')
    console.log(img)
    canvas.width = img.width
    canvas.height = img.height
    ctx.drawImage(img, 0, 0)
    //this.drawPatientDots()
    window.requestAnimationFrame(this.drawPatientDots)
  }

  resetCanvas = () => {
    let img = document.getElementById("ward")
    let canvas = document.getElementById("canvas")
    let ctx = canvas.getContext('2d')
    console.log(img)
    canvas.width = img.width
    canvas.height = img.height
    ctx.drawImage(img, 0, 0)
  }

  drawPatientDots = () => {
    let canvas = document.getElementById("canvas")
    let ctx = canvas.getContext('2d')
    this.resetCanvas()
    let t = (Date.now() % 30) / 10
    for (let coord of this.patient_locs){
      console.log(t)
      ctx.fillStyle = "#05ff1a"
      ctx.beginPath()
      ctx.arc(coord[0], coord[1], 20 + t, 0, 2 * Math.PI);
      ctx.fill()
    }
    window.requestAnimationFrame(this.drawPatientDots)
  }

  gotoMap = () => {
    this.props.history.push('/patients');
  }

  render() {
    return (
    <div style={{"paddingLeft": "4%"}}>
      <img id="ward" src={ward} style={{"display": "none"}} onLoad={this.onLoadImg} ></img>
      <canvas id="canvas" onClick={this.gotoMap}></canvas>
    </div>);
  }
}
