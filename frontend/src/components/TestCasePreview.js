import React from 'react';
import { Tabs, Tab, Table } from 'react-bootstrap';

function TestCasePreview({ testCases }) {
  // 최대 10개까지만 표시
  const casesToShow = testCases.slice(0, 10);
  const columns = ['TID', '대분류', '중분류', '소분류', 'Precondition', 'Test_Step', 'Expected_Result'];

  return (
    <div className="test-case-preview mb-4">
      <Tabs defaultActiveKey="preview" className="mb-3">
        <Tab eventKey="preview" title="미리보기">
          <div className="alert alert-info">생성된 테스트 케이스 미리보기 (최대 10개)</div>
          <div className="table-responsive border rounded">
            <Table bordered striped hover>
              <thead>
                <tr>
                  {columns.map(col => (
                    <th key={col}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {casesToShow.map((tc, idx) => (
                  <tr key={idx}>
                    {columns.map(col => (
                      <td key={col} dangerouslySetInnerHTML={{ 
                        __html: tc[col] ? tc[col].replace(/\n/g, '<br>') : '' 
                      }} />
                    ))}
                  </tr>
                ))}
                {testCases.length > 10 && (
                  <tr>
                    <td colSpan={columns.length} className="text-center text-muted">
                      ... 그 외 {testCases.length - 10}개의 테스트 케이스가 더 있습니다. 전체 내용은 Excel 파일을 확인하세요.
                    </td>
                  </tr>
                )}
              </tbody>
            </Table>
          </div>
          <p><small className="text-muted">* Excel 파일에서 모든 테스트 케이스를 확인할 수 있습니다.</small></p>
        </Tab>
      </Tabs>
    </div>
  );
}

export default TestCasePreview; 