import React, { Component } from 'react';
import PatientsCard from './PatientsCard';
import "../css/app.css";

export default class Main extends Component {
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
