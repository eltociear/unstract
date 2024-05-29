import {
  ExceptionOutlined,
  FullscreenExitOutlined,
  LeftOutlined,
  RightOutlined,
} from "@ant-design/icons";
import { Button, Collapse, Layout, Modal, Typography } from "antd";
import { useEffect, useState } from "react";
import { Outlet } from "react-router-dom";
import "./PageLayout.css";

import SideNavBar from "../../components/navigations/side-nav-bar/SideNavBar.jsx";
import { TopNavBar } from "../../components/navigations/top-nav-bar/TopNavBar.jsx";
import { Footer } from "antd/es/layout/layout.js";
import { DisplayLogs } from "../../components/custom-tools/display-logs/DisplayLogs.jsx";
import { LogsLabel } from "../../components/agency/logs-label/LogsLabel.jsx";
import { useResize } from "../../hooks/useResize.jsx";
import axios from "axios";
import { useSessionStore } from "../../store/session-store.js";
import { useSocketLogsStore } from "../../store/socket-logs-store.js";

function PageLayout() {
  const [showLogsModal, setShowLogsModal] = useState(false);
  const [activeKey, setActiveKey] = useState([]);
  const { height, enableResize, setHeight } = useResize({ minHeight: 50 });
  const { sessionDetails } = useSessionStore();
  const initialCollapsedValue =
    JSON.parse(localStorage.getItem("collapsed")) || false;
  const [collapsed, setCollapsed] = useState(initialCollapsedValue);

  const getLogs = async () => {
    const requestOptions = {
      method: "GET",
      url: `/api/v1/unstract/${sessionDetails.orgId}/logs/`,
      headers: {
        "X-CSRFToken": sessionDetails.csrfToken,
      },
    };

    try {
      const response = await axios(requestOptions);
      return response.data;
    } catch (error) {
      return;
    }
  };

  const closeLogsModal = () => {
    setShowLogsModal(false);
  };
  const handleCollapse = (keys) => {
    setActiveKey(keys);
    setHeight(keys.length > 0 ? 200 : 50);
  };

  const getItems = () => [
    {
      key: "1",
      label:
        activeKey?.length > 0 ? (
          <>
            <div
              aria-hidden="true"
              style={{
                position: "absolute",
                width: "100%",
                top: 0,
                cursor: "row-resize",
                height: "10px",
              }}
              onMouseDown={enableResize}
              onClick={(e) => e.stopPropagation()}
            />
            <LogsLabel />
          </>
        ) : (
          <Typography className="logs-title">
            <ExceptionOutlined />
            Logs
          </Typography>
        ),
      children: (
        <div className="agency-ide-logs" style={{ height: height - 50 }}>
          <DisplayLogs />
        </div>
      ),
    },
  ];

  useEffect(() => {
    localStorage.setItem("collapsed", JSON.stringify(collapsed));
    if (activeKey.length > 0) {
      getLogs().then((res) =>
        useSocketLogsStore.setState(() => ({
          logs: [...res.data],
        }))
      );
    }
  }, [collapsed, activeKey]);

  return (
    <div className="landingPage">
      <TopNavBar />
      <Layout>
        <SideNavBar collapsed={collapsed} />
        <Layout>
          <Button
            shape="circle"
            size="small"
            icon={collapsed ? <RightOutlined /> : <LeftOutlined />}
            onClick={() => setCollapsed(!collapsed)}
            className="collapse_btn"
          />
          <Outlet />
          <Footer className="log-footer">
            <Collapse
              className="ide-collapse-panel"
              size="small"
              activeKey={activeKey}
              items={getItems()}
              expandIconPosition="end"
              onChange={handleCollapse}
              bordered={false}
              style={{ height: height }}
            />
            <Modal
              title="Logs"
              open={showLogsModal}
              onCancel={closeLogsModal}
              className="agency-ide-log-modal"
              footer={null}
              width={1000}
              closeIcon={<FullscreenExitOutlined />}
            >
              <LogsLabel />
              <div className="agency-ide-logs">
                <DisplayLogs />
              </div>
            </Modal>
          </Footer>
        </Layout>
      </Layout>
    </div>
  );
}

export { PageLayout };
