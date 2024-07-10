import React from "react";
import { useEffect,useState } from "react";

function SignUp(){
    return(
        <div className="signup">
            <h1> Wecome to Careconnect.</h1>
            <div class="mb-3">
                <label for="exampleFormControlInput1" class="form-label">Username</label>
                <input type="text" class="form-control" id="exampleFormControlInput1" placeholder="Enter your user name"></input>
            </div>
            <div class="mb-3">
                <label for="exampleFormControlInput1" class="form-label">First name</label>
                <input type="text" class="form-control" id="exampleFormControlInput1" placeholder="Enter your first name"></input>
            </div>
            <div class="mb-3">
                <label for="exampleFormControlInput1" class="form-label">Last name</label>
                <input type="text" class="form-control" id="exampleFormControlInput1" placeholder="Enter your last name"></input>
            </div>
            <div class="mb-3">
                <label for="exampleFormControlInput1" class="form-label">Date of Birth</label>
                <input type="date" class="form-control" id="exampleFormControlInput1" placeholder="Enter your DOB"></input>
            </div>
            <div class="mb-3">
                <label for="exampleFormControlInput1" class="form-label">Contat number</label>
                <input type="text" class="form-control" id="exampleFormControlInput1" placeholder="Enter your number"></input>
            </div>
            <div class="mb-3">
                <label for="exampleFormControlInput1" class="form-label">Email address</label>
                <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com"></input>
            </div>
            <div class="mb-3">
                <label for="exampleFormControlInput1" class="form-label">Password</label>
                <input type="password" class="form-control" id="exampleFormControlInput1" placeholder="Enter your password"></input>
            </div>
            
        </div>
    );
}
export default SignUp;
