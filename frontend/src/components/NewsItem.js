import React from "react";
import "./NewsItem.css";

const NewsItem = (props) => {
  let { id, title, description, imageUrl, newsUrl, author, date, source } = props;
  const handleAnchorClick = event => {
    fetch(process.env.REACT_APP_BACKEND_ENDPOINT + 'watch/' + id, {credentials: 'include'}).then((response) =>{console.log(response)});
  };
  return (
    <div className="my-3">
      <div className="card">
        <div
          style={{
            display: "flex",
            justifyContent: "flex-end",
            position: "absolute",
            right: "0",
          }}
        >
          <span className="badge rounded-pill bg-danger"> {source} </span>
        </div>
        <img
          src={
            !imageUrl
              ? "https://fdn.gsmarena.com/imgroot/news/21/08/xiaomi-smart-home-india-annoucnements/-476x249w4/gsmarena_00.jpg"
              : imageUrl
          }
          className="card-img-top"
          alt="..."
        />
        <div className="card-body">
          <h5 className="card-title">
            <b>{title}</b>{" "}
          </h5>
          <p className="card-text">{description}</p>
          <p className="card-text">
            <small className="text-muted">
              By {!author ? "Unknown" : author} on{" "}
              {new Date(date).toGMTString()}
            </small>
          </p>
          <a
            rel="noreferrer"
            href={newsUrl}
            target="_blank"
            className="btn btn-sm btn-dark"
            onClick={handleAnchorClick}
          >
            Read More
          </a>
        </div>
      </div>
    </div>
  );
};

export default NewsItem;
