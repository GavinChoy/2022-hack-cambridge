import React, { Component } from 'react';
import "../css/app.css";

export default class RightSideNav extends Component {
    constructor(props) {
        super(props);
        const d = new Date()
        this.state = {
            time: `${d.getHours()}:${d.getMinutes()<10? `0${d.getMinutes()}` : d.getMinutes()}`,
            date: `${d.getDate()}/${d.getMonth()+1 < 10? `0${d.getMonth()+1}`: d.getMinutes()}/${d.getFullYear()}`,
        }
        setInterval(this.setTime, 1000)
    }

    setTime = () => {
        const d = new Date()
        if (d.getSeconds() === 0) {
            this.setState({time: `${d.getHours()}:${d.getMinutes()<10? `0${d.getMinutes()}` : d.getMinutes()}`, date: `${d.getDate()}/${d.getMonth()+1 < 10? `0${d.getMonth()+1}`: d.getMinutes()}/${d.getFullYear()}`})
        }
    }

  render() {
    return (
    <div className="rsn">
        <div className="rsn-title-2"><span>Today's Schedule</span></div>
        <div className="rsn-title">
            <span className="rsn-title">{this.state.date}</span>
            <span className="rsn-title mr-3">{this.state.time}</span>
        </div>
    </div>);
  }
}
