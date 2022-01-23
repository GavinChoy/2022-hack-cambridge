import React, { Component } from 'react';
import PatientsCard from './PatientsCard';
import "../css/app.css";

export default class Main extends Component {

  componentDidMount() {
    this.poll()
  }

  poll = () => {
    const data = {
      "request": "client"
    }
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('Accept', 'application/json');
    fetch('https://europe-west2-dementiaassist.cloudfunctions.net/transcription_sentiment', {
      headers: headers,
      mode: "cors",
      method: "POST",
      body: JSON.stringify(data),
    }).then((res)=>{
      // if (res.status !== 203) console.log(res) 
      console.log(res)
      return res.json()
      // this.poll()
    }).then(data=>console.log(data)).catch((err)=>{
      console.log(err)
      this.poll()
    }
      )
  }

  render() {
    return (
    <div className="patients-container">
      <div className="p-t">Patients</div>
      <PatientsCard />
      <PatientsCard />
      <PatientsCard />
    </div>
    );
  }
}
