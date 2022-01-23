import React, { Component } from 'react';
import PatientsCard from './PatientsCard';
import "../css/app.css";

export default class Main extends Component {

  state= {

  }

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
    }).then(data=>this.setState({patients: data})).catch((err)=>{
      console.log(err)
      this.poll()
    }
      )
  }

  render() {
    if (this.state.patients) console.log(this.state.patients)
    return (
    <div className="patients-container">
      <div className="p-t">Patients</div>
      {this.state.patients && Object.keys(this.state.patients).map((key, index) => {
        {console.log(this.state.patients[key][0])}
        return (
        <PatientsCard
          key={index}
          name={key}
          problems={this.state.patients[key][0]['problem']}
          actions={this.state.patients[key][0]['suggested_action']}
          text={this.state.patients[key][0]['full_text']}
          severity={this.state.patients[key][0]['severity']}
        />)
      })}
      {/* <PatientsCard /> */}
    </div>
    );
  }
}
