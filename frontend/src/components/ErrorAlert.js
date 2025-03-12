import React from 'react';
import { Alert, Button } from 'react-bootstrap';

function ErrorAlert({ message, onRetry }) {
  return (
    <Alert variant="danger" className="my-4">
      <Alert.Heading>오류 발생</Alert.Heading>
      <p>{message}</p>
      <div className="d-flex justify-content-end">
        <Button variant="outline-danger" onClick={onRetry}>
          다시 시도
        </Button>
      </div>
    </Alert>
  );
}

export default ErrorAlert; 