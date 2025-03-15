import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from '../static/AuthContext';
import { useNavigate } from 'react-router-dom';
import { MdWork, MdLibraryBooks, MdAssessment } from "react-icons/md";
import { PiCertificateFill } from "react-icons/pi";

function Navbar() {
    const [loggedOut, setLoggedOut] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        if (loggedOut) {
            navigate("/login");
            window.location.reload();
        }
    }, [loggedOut, navigate]); 
    const authHandler = useAuth(); 
    const logOutRedirect = () => {
        authHandler.logout();
        setLoggedOut(true);
    }
    return (
      <div className="d-flex flex-column flex-shrink-0 p-3 bg-body-tertiary h-100 sidebar" style={{ width: '100%'}}>
          
          {/* Sidebar menu */}
          <ul className="nav nav-pills flex-column mb-auto">
              <li className="nav-item mt-5">
                  <Link to="/courses" className="nav-link">
                      <svg className="bi pe-none me-2" width="16" height="16"><use xlink:href="#home"/></svg>
                      Courses <MdLibraryBooks />
                  </Link>
              </li>
              <li className="nav-item">
                  <Link to="/job-portal" className="nav-link link-body-emphasis">
                      <svg className="bi pe-none me-2" width="16" height="16"><use xlink:href="#speedometer2"/></svg>
                      Jobs <MdWork/>
                  </Link>
              </li>
              <li className="nav-item">
                  <Link to="/assessments" className="nav-link link-body-emphasis">
                      <svg className="bi pe-none me-2" width="16" height="16"><use xlink:href="#grid"/></svg>
                      Assessments <MdAssessment />
                  </Link>
              </li>
              <li className="nav-item">
                  <Link to="/certificates" className="nav-link link-body-emphasis">
                      <svg className="bi pe-none me-2" width="16" height="16"><use xlink:href="#table"/></svg>
                      Certificates <PiCertificateFill  />
                  </Link>
              </li>
          </ul>
          
          <hr />
          
          {/* Dropdown for profile */}
          <div className="dropdown">
              <a href="#" className="d-flex align-items-center link-body-emphasis text-decoration-none dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                  <img src="https://github.com/mdo.png" alt="" width="32" height="32" className="rounded-circle me-2" />
                  <strong>mdo</strong>
              </a>
              <ul className="dropdown-menu text-small shadow">
                  <li><Link to="/profile" className="dropdown-item">Profile</Link></li>
                  <li><a className="dropdown-item" href="#" onClick={logOutRedirect}>Sign out</a></li>
              </ul>
          </div>
      </div>
  );
}

export default Navbar;
