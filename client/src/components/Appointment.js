import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import './Appointment.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const Appointment = () => {
    const [date, setDate] = useState(new Date());
    const [appointments, setAppointments] = useState([]);
    const [selectedAppointment, setSelectedAppointment] = useState(null);
    const [details, setDetails] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    useEffect(() => {
        setLoading(true);
        axios.get('http://127.0.0.1:5555/appointments')
            .then(response => {
                setAppointments(response.data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching appointments:', error);
                setError('Error fetching appointments');
                alert('Error fetching appointments');
                setLoading(false);
            });
    }, []);

    const handleFormValidation = () => {
        if (!details) {
            setError('Appointment details are required.');
            alert('Appointment details are required.');
            return false;
        }
        setError('');
        return true;
    };

    const createAppointment = () => {
        if (!handleFormValidation()) return;

        setLoading(true);
        axios.post('http://127.0.0.1:5555/appointments', {
            appointment_date: date.toISOString(),
            reason: details,
            status: 'Scheduled'
        })
            .then(response => {
                setAppointments([...appointments, response.data]);
                setDetails('');
                setSuccess('Appointment created successfully');
                alert('Appointment created successfully');
                setLoading(false);
            })
            .catch(error => {
                console.error('Error creating appointment:', error);
                setError('Error creating appointment');
                alert('Error creating appointment');
                setLoading(false);
            });
    };

    const updateAppointment = () => {
        if (!handleFormValidation()) return;

        setLoading(true);
        axios.put(`http://127.0.0.1:5555/appointments/${selectedAppointment}`, {
            appointment_date: date.toISOString(),
            reason: details,
            status: 'Rescheduled'
        })
            .then(response => {
                const updatedAppointments = appointments.map(appointment =>
                    appointment.id === selectedAppointment ? response.data : appointment
                );
                setAppointments(updatedAppointments);
                setSelectedAppointment(null);
                setDetails('');
                setSuccess('Appointment updated successfully');
                alert('Appointment updated successfully');
                setLoading(false);
            })
            .catch(error => {
                console.error('Error updating appointment:', error);
                setError('Error updating appointment');
                alert('Error updating appointment');
                setLoading(false);
            });
    };

    const deleteAppointment = (id) => {
        setLoading(true);
        axios.delete(`http://127.0.0.1:5555/appointments/${id}`)
            .then(() => {
                setAppointments(appointments.filter(appointment => appointment.id !== id));
                setSuccess('Appointment deleted successfully');
                alert('Appointment deleted successfully');
                setLoading(false);
            })
            .catch(error => {
                console.error('Error deleting appointment:', error);
                setError('Error deleting appointment');
                alert('Error deleting appointment');
                setLoading(false);
            });
    };

    return (
        <div className="appointment-container container">
            <h2>Manage Appointments</h2>
            {loading && <div className="alert alert-info">Loading...</div>}
            {error && <div className="alert alert-danger">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}

            <Calendar
                onChange={setDate}
                value={date}
            />
            <div className="form-group mt-3">
                <input
                    type="text"
                    className="form-control"
                    placeholder="Appointment Details"
                    value={details}
                    onChange={(e) => setDetails(e.target.value)}
                />
            </div>
            {selectedAppointment !== null ? (
                <button className="btn btn-primary mt-2" onClick={updateAppointment}>
                    Update Appointment
                </button>
            ) : (
                <button className="btn btn-success mt-2" onClick={createAppointment}>
                    Create Appointment
                </button>
            )}
            <h3 className="mt-4">Appointments</h3>
            <ul className="list-group">
                {appointments.map(appointment => (
                    <li className="list-group-item d-flex justify-content-between align-items-center" key={appointment.id}>
                        <div>
                            <strong>{new Date(appointment.appointment_date).toLocaleString()}</strong>: {appointment.reason}
                        </div>
                        <div>
                            <button className="btn btn-warning btn-sm mr-2" onClick={() => {
                                setSelectedAppointment(appointment.id);
                                setDetails(appointment.reason);
                                setDate(new Date(appointment.appointment_date));
                            }}>
                                Edit
                            </button>
                            <button className="btn btn-danger btn-sm" onClick={() => deleteAppointment(appointment.id)}>
                                Delete
                            </button>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Appointment;
