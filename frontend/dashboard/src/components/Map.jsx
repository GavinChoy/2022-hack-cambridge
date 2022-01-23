import React, { Component } from 'react';
import "./patient_ward.png" 

export default class Map extends Component {
  
  patient_locs = [[150, 50, "#eb4034"], [50, 130, "#eb4034"], [52, 375, "#eb7a34"], [150, 475, "#05ff1a"], [360, 475, "#eb7a34"]]

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
      ctx.fillStyle = coord[2]
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
    <div style={{"paddingLeft": "4%", "paddingTop": "4%"}}>
      <img id="ward" src={require('./patient_ward.png')} style={{display: "none"}} onLoad={this.onLoadImg} ></img>
      <canvas id="canvas" onClick={this.gotoMap}></canvas>
    </div>);
  }
}
