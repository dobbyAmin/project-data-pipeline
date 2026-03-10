# Online-Retail-Data-Pipeline
Academic Project in Data Pipeline Architecture

## คำอธิบาย (Description)
โปรเจกต์นี้เป็นการจำลองและสร้าง Data Pipeline แบบครบวงจร (End-to-End) สำหรับการจัดการข้อมูลการขายสินค้าออนไลน์ (Online Retail) โดยเริ่มต้นตั้งแต่กระบวนการนำเข้าข้อมูล (Data Ingestion) ตรวจสอบความถูกต้อง นำไปผ่านการแปลงรูป (Transformation) เพื่อจัดเก็บในรูปแบบที่พร้อมสำหรับการวิเคราะห์ใน Data Marts และปิดท้ายด้วยการส่งอีเมลแจ้งเตือนเมื่อข้อมูลพร้อมใช้งานสำหรับทีม BI (Business Intelligence)

## Tech Stack
- **Apache Airflow**: เป็น Orchestrator หลักสำหรับจัดการ Workflow, เรียงลำดับขั้นตอน (DAGs) และกำหนดเวลาการทำงานของ Pipeline เป็นรอบวัน (Daily `0 3 * * *`)
- **dbt (Data Build Tool)**: ใช้สำหรับการทำ Data Transformation ในระดับ Core และระดับ Data Marts เพื่อให้ได้ข้อมูลที่แม่นยำและตอบโจทย์ธุรกิจ
- **Great Expectations**: เครื่องมือสำหรับ Data Quality Assessment และ Validation เพื่อตรวจสอบคุณภาพของข้อมูลในทุก ๆ ขั้นตอน (Raw, Core, และ Marts)
- **PostgreSQL**: ทำหน้าที่เป็น Data Warehouse หลักในการเก็บข้อมูลทั้งหมดตั้งแต่ Staging Area ไปจนถึง Data Marts
- **Docker & Docker Compose**: ใช้สำหรับ Containerization เพื่อให้จัดการ dependencies ง่าย ดึงขึ้นมาใช้งานได้อย่างรวดเร็ว ครอบคลุมทั้ง Airflow, Postgres และ pgAdmin

## การทำงานโดยภาพรวม (Overall Architecture)
Data Pipeline ถูกออกแบบให้รันเป็นลำดับชั้น 4 ขั้นตอนหลัก:

1. **Ingestion (Data Loading & Filtering)**
   - นำเข้าข้อมูลการขายจากไฟล์ `.csv` (`online_retail.csv`)
   - กรองข้อมูลเบื้องต้น เช่น Quantity > 0, UnitPrice > 0, ตรวจสอบรูปแบบของ Invoice\StockCode และต้องระบุ CustomerID
   - ข้อมูลที่ผ่านเกณฑ์จะเก็บในตาราง `raw_data` และส่วนที่มีปัญหาจะถูกแยกไปที่ตาราง `data_issues` จัดเก็บอยู่ใน Schema `staging`
   - ตรวจสอบคุณภาพ (`raw_data_checkpoint`) ด้วย Great Expectations 
2. **Core Transformation**
   - รันโมเดล `dbt run --select core` เพื่อทำความสะอาด จัดเรียง และสร้างโครงสร้างตารางข้อมูลที่เป็นมาตรฐาน 
   - ตรวจสอบคุณภาพระดับ Core (`core_checkpoint`) ด้วย Great Expectations
3. **Data Marts (การเตรียมข้อมูลเพื่อให้ฝั่งธุรกิจใช้งาน)**
   - รันโมเดล `dbt run --select marts` เพื่อแยกข้อมูลออกเป็นส่วน ๆ ตามวัตถุประสงค์ เช่น `sales_mart` และ `customer_mart` 
   - ตรวจสอบคุณภาพที่พร้อมใช้งาน (`mart_sales_checkpoint`, `mart_customer_checkpoint`) ด้วย Great Expectations
4. **Publish (Data Ready & Alerts)**
   - เมื่อสร้าง Data Marts เสร็จสมบูรณ์ Airflow จะส่งอีเมลอัตโนมัติไปยังทีม BI (`bi@online_retail.com`) เพื่อเปิดให้ทีมสามารถนำข้อมูลไปวิเคราะห์หรือทำ Dashboard ต่อไป

## โครงสร้าง Project (Project Structure)
- `airflow/dags/online_retail.py`: โค้ดที่ใช้ควบคุม Data Pipeline ทำงานร่วมกับ Airflow
- `dbt/` & `dbt_root/`: ประกอบด้วย dbt project และ settings การเชื่อมต่อ (`profiles.yml`)
- `gx_retail/`: ประกอบด้วยการตั้งค่าชุดเครื่องมือของ Great Expectations
- `docker-compose.yml`: ไฟล์กำหนด orchestration สำหรับ containers ทั้งหมด (PostgreSQL Database, pgAdmin UI, Initialization และ Airflow Environment)
- `dockerfile.airflow`: Dockerfile สร้าง image สำหรับ Airflow และส่วนขยายเพิ่มเติมที่โปรเจกต์ต้องใช้

## วิธีการใช้งานและรันระบบ (How to Run)
1. รันคอนเทนเนอร์ทั้งหมดผ่าน Docker Compose ในโหมด deatched:
   ```bash
   docker-compose up -d --build
   ```
2. เมื่อระบบทั้งหมดพร้อมทำงาน สามารถเข้าถึงบริการได้ตาม Port ดังนี้:
   - **Airflow UI**: `http://localhost:18080`
   - **pgAdmin**: `http://localhost:8888`
   - **PostgreSQL**: `localhost:5432` สำหรับทดสอบ query ข้อมูล
3. เข้า Airflow UI (ชื่อผู้ใช้ `admin`, รหัสผ่าน `admin`) นำ DAG ชื่อ **`Online_Retail_Pipeline`** เปลี่ยนสถานะเป็น Active เพื่อเริ่มต้นการทำงานของ ET(L)L Pipeline นี้
