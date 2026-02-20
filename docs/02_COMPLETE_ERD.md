# دیاکو MES - نمودار ERD کامل پایگاه داده
## Complete Entity Relationship Diagram

---

## نکته معماری: آماده‌سازی برای AI

تمام جداول تولیدی دارای فیلدهای زیر هستند تا در آینده ماژول‌های هوش مصنوعی بتوانند داده‌های سری زمانی تحلیل کنند:
- `created_at` (DATETIME) - زمان دقیق ثبت
- `shift` (ENUM) - شیفت کاری (صبح/عصر/شب)
- `operator_id` (FK) - اپراتور ثبت‌کننده
- `machine_id` (FK) - شناسه ماشین
- فیلدهای JSON اضافی (`metadata`) برای داده‌های سنسوری آینده

---

## 1. CORE APP (هسته مشترک)

### 1.1 core_machine (ماشین‌آلات)
```sql
CREATE TABLE core_machine (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    code            VARCHAR(20) UNIQUE NOT NULL,          -- کد ماشین: CR-01, RG-15
    name            VARCHAR(100) NOT NULL,                -- نام ماشین
    machine_type    ENUM('blowroom','carding','passage','finisher','ring','dyeing','boiler','dryer') NOT NULL,
    manufacturer    VARCHAR(100),                         -- سازنده
    model           VARCHAR(100),                         -- مدل
    year_installed  SMALLINT,                             -- سال نصب
    location        VARCHAR(100),                         -- محل استقرار (سالن)
    status          ENUM('active','inactive','maintenance','decommissioned') DEFAULT 'active',
    specs           JSON,                                 -- مشخصات فنی (برای AI)
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_type (machine_type),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 1.2 core_shift (شیفت کاری)
```sql
CREATE TABLE core_shift (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(50) NOT NULL,           -- صبح / عصر / شب
    code        VARCHAR(5) NOT NULL UNIQUE,     -- A / B / C
    start_time  TIME NOT NULL,                  -- 06:00
    end_time    TIME NOT NULL,                  -- 14:00
    is_active   BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 1.3 core_productionlog (لاگ تولید مشترک - Abstract Pattern)
> این جدول الگوی پایه‌ای است که هر ماژول تولیدی از آن ارث‌بری می‌کند

```sql
-- این یک Abstract Model است و جدول مستقلی ایجاد نمی‌شود
-- هر ماژول فیلدهای زیر را به ارث می‌برد:
--   machine_id      BIGINT FK → core_machine
--   operator_id     BIGINT FK → accounts_user
--   shift_id        BIGINT FK → core_shift
--   production_date DATE
--   created_at      DATETIME
--   updated_at      DATETIME
--   notes           TEXT
--   metadata        JSON (برای AI)
```

### 1.4 core_auditlog (لاگ تغییرات)
```sql
CREATE TABLE core_auditlog (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id         BIGINT NOT NULL,
    action          ENUM('create','update','delete') NOT NULL,
    table_name      VARCHAR(100) NOT NULL,
    record_id       BIGINT NOT NULL,
    old_values      JSON,
    new_values      JSON,
    ip_address      VARCHAR(45),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_table_record (table_name, record_id),
    INDEX idx_user (user_id),
    INDEX idx_created (created_at),
    FOREIGN KEY (user_id) REFERENCES accounts_user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 1.5 core_notification (اعلان‌ها)
```sql
CREATE TABLE core_notification (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    recipient_id    BIGINT NOT NULL,
    title           VARCHAR(200) NOT NULL,
    message         TEXT NOT NULL,
    notif_type      ENUM('info','warning','danger','success','maintenance') NOT NULL,
    is_read         BOOLEAN DEFAULT FALSE,
    link            VARCHAR(500),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_recipient_read (recipient_id, is_read),
    FOREIGN KEY (recipient_id) REFERENCES accounts_user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 2. ACCOUNTS APP (کاربران و دسترسی)

### 2.1 accounts_user (کاربران)
```sql
CREATE TABLE accounts_user (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(150) UNIQUE NOT NULL,
    password        VARCHAR(128) NOT NULL,
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    national_code   VARCHAR(10) UNIQUE,               -- کد ملی
    phone           VARCHAR(15),
    email           VARCHAR(254),
    role            ENUM('admin','manager','supervisor','operator','viewer') NOT NULL DEFAULT 'operator',
    department      ENUM('production','warehouse','dyeing','maintenance','quality','office') DEFAULT 'production',
    is_active       BOOLEAN DEFAULT TRUE,
    is_staff        BOOLEAN DEFAULT FALSE,
    is_superuser    BOOLEAN DEFAULT FALSE,
    avatar          VARCHAR(500),
    last_login      DATETIME,
    date_joined     DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_role (role),
    INDEX idx_department (department)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 3. INVENTORY APP (انبار)

### 3.1 inventory_fibercategory (دسته‌بندی الیاف)
```sql
CREATE TABLE inventory_fibercategory (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,          -- پلی‌استر، اکریلیک، پشم، ...
    code        VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    is_active   BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 3.2 inventory_fiberstock (موجودی الیاف)
```sql
CREATE TABLE inventory_fiberstock (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    category_id     BIGINT NOT NULL,
    batch_number    VARCHAR(50) NOT NULL,                -- شماره بچ/لات
    lot_number      VARCHAR(50),                         -- شماره لات تامین‌کننده
    supplier        VARCHAR(200),                        -- تامین‌کننده
    color_raw       VARCHAR(100),                        -- رنگ اولیه الیاف
    denier          DECIMAL(8,2),                        -- دنیر (ضخامت الیاف)
    staple_length   DECIMAL(8,2),                        -- طول الیاف (mm)
    initial_weight  DECIMAL(12,3) NOT NULL,              -- وزن اولیه (کیلوگرم)
    current_weight  DECIMAL(12,3) NOT NULL,              -- وزن فعلی
    unit_price      DECIMAL(15,0),                       -- قیمت واحد (ریال)
    received_date   DATE NOT NULL,                       -- تاریخ ورود (FIFO key)
    expiry_date     DATE,
    warehouse_loc   VARCHAR(50),                         -- محل انبار (ردیف-قفسه)
    status          ENUM('available','reserved','consumed','returned') DEFAULT 'available',
    quality_grade   ENUM('A','B','C') DEFAULT 'A',
    notes           TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_batch (batch_number),
    INDEX idx_category (category_id),
    INDEX idx_status (status),
    INDEX idx_received_date (received_date),             -- برای FIFO
    INDEX idx_fifo (status, received_date),              -- ایندکس ترکیبی FIFO
    FOREIGN KEY (category_id) REFERENCES inventory_fibercategory(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 3.3 inventory_dyestock (موجودی رنگ)
```sql
CREATE TABLE inventory_dyestock (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,               -- نام رنگ
    code            VARCHAR(50) UNIQUE NOT NULL,          -- کد رنگ
    color_family    VARCHAR(50),                         -- خانواده رنگ (قرمز، آبی...)
    dye_type        ENUM('reactive','disperse','acid','vat','direct') NOT NULL,
    manufacturer    VARCHAR(200),
    batch_number    VARCHAR(50) NOT NULL,
    initial_weight  DECIMAL(12,3) NOT NULL,
    current_weight  DECIMAL(12,3) NOT NULL,
    unit            ENUM('kg','g','liter') DEFAULT 'kg',
    unit_price      DECIMAL(15,0),
    received_date   DATE NOT NULL,
    expiry_date     DATE,
    storage_temp    DECIMAL(5,2),                        -- دمای نگهداری
    status          ENUM('available','reserved','consumed','expired') DEFAULT 'available',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status_date (status, received_date),
    INDEX idx_dye_type (dye_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 3.4 inventory_chemicalstock (موجودی مواد شیمیایی - اسید و غیره)
```sql
CREATE TABLE inventory_chemicalstock (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    code            VARCHAR(50) UNIQUE NOT NULL,
    chemical_type   ENUM('acid','alkali','salt','softener','fixative','auxiliary','other') NOT NULL,
    manufacturer    VARCHAR(200),
    batch_number    VARCHAR(50) NOT NULL,
    initial_amount  DECIMAL(12,3) NOT NULL,
    current_amount  DECIMAL(12,3) NOT NULL,
    unit            ENUM('kg','g','liter','ml') DEFAULT 'kg',
    unit_price      DECIMAL(15,0),
    concentration   DECIMAL(5,2),                        -- غلظت (درصد)
    received_date   DATE NOT NULL,
    expiry_date     DATE,
    msds_file       VARCHAR(500),                        -- فایل برگه ایمنی
    status          ENUM('available','reserved','consumed','expired') DEFAULT 'available',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status_date (status, received_date),
    INDEX idx_chemical_type (chemical_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 3.5 inventory_stocktransaction (تراکنش‌های انبار)
```sql
CREATE TABLE inventory_stocktransaction (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    stock_type      ENUM('fiber','dye','chemical') NOT NULL,
    stock_id        BIGINT NOT NULL,                     -- FK polymorphic
    transaction_type ENUM('receive','issue','return','adjust','waste') NOT NULL,
    quantity        DECIMAL(12,3) NOT NULL,
    unit            VARCHAR(10) NOT NULL,
    reference_type  VARCHAR(50),                         -- blowroom_batch, dyeing_batch, ...
    reference_id    BIGINT,                              -- شناسه مرجع مصرف
    performed_by_id BIGINT NOT NULL,
    notes           TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_stock (stock_type, stock_id),
    INDEX idx_reference (reference_type, reference_id),
    INDEX idx_date (created_at),
    FOREIGN KEY (performed_by_id) REFERENCES accounts_user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 4. ORDERS APP (سفارشات و رنگ)

### 4.1 orders_customer (مشتریان)
```sql
CREATE TABLE orders_customer (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    company         VARCHAR(200),
    phone           VARCHAR(15),
    mobile          VARCHAR(15),
    email           VARCHAR(254),
    address         TEXT,
    city            VARCHAR(100),
    province        VARCHAR(100),
    tax_id          VARCHAR(20),                         -- شناسه مالیاتی
    credit_limit    DECIMAL(18,0) DEFAULT 0,
    is_active       BOOLEAN DEFAULT TRUE,
    notes           TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 4.2 orders_colorshade (شِید رنگی)
```sql
CREATE TABLE orders_colorshade (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    code            VARCHAR(50) UNIQUE NOT NULL,         -- کد شید: SH-1024
    name            VARCHAR(200) NOT NULL,               -- نام رنگ
    color_hex       VARCHAR(7),                          -- #FF5733
    recipe          JSON,                                -- فرمول رنگ (نسبت مواد)
    image           VARCHAR(500),                        -- تصویر نمونه رنگ
    is_approved     BOOLEAN DEFAULT FALSE,
    approved_by_id  BIGINT,
    approved_at     DATETIME,
    notes           TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_approved (is_approved),
    FOREIGN KEY (approved_by_id) REFERENCES accounts_user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 4.3 orders_colorapprovalhistory (تاریخچه تایید رنگ)
```sql
CREATE TABLE orders_colorapprovalhistory (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    color_shade_id  BIGINT NOT NULL,
    customer_id     BIGINT NOT NULL,
    status          ENUM('submitted','customer_review','approved','rejected','revised') NOT NULL,
    sample_image    VARCHAR(500),                        -- تصویر نمونه ارسالی
    customer_feedback TEXT,
    reviewed_by_id  BIGINT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_shade_status (color_shade_id, status),
    FOREIGN KEY (color_shade_id) REFERENCES orders_colorshade(id),
    FOREIGN KEY (customer_id) REFERENCES orders_customer(id),
    FOREIGN KEY (reviewed_by_id) REFERENCES accounts_user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 4.4 orders_order (سفارش)
```sql
CREATE TABLE orders_order (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_number    VARCHAR(20) UNIQUE NOT NULL,          -- شماره سفارش: ORD-14030115-001
    customer_id     BIGINT NOT NULL,
    color_shade_id  BIGINT,
    yarn_type       VARCHAR(100),                        -- نوع نخ درخواستی
    yarn_count      VARCHAR(50),                         -- نمره نخ
    quantity_kg     DECIMAL(12,3) NOT NULL,               -- مقدار (کیلوگرم)
    unit_price      DECIMAL(15,0),
    total_price     DECIMAL(18,0),
    delivery_date   DATE,                                -- تاریخ تحویل
    priority        ENUM('low','normal','high','urgent') DEFAULT 'normal',
    status          ENUM('draft','confirmed','in_production','quality_check','ready','delivered','cancelled') DEFAULT 'draft',
    progress_pct    TINYINT DEFAULT 0,                   -- درصد پیشرفت (0-100)
    notes           TEXT,
    created_by_id   BIGINT NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_customer (customer_id),
    INDEX idx_status (status),
    INDEX idx_delivery (delivery_date),
    INDEX idx_priority_status (priority, status),
    FOREIGN KEY (customer_id) REFERENCES orders_customer(id),
    FOREIGN KEY (color_shade_id) REFERENCES orders_colorshade(id),
    FOREIGN KEY (created_by_id) REFERENCES accounts_user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 5. BLOWROOM APP (حلاجی)

### 5.1 blowroom_batch (بچ حلاجی)
```sql
CREATE TABLE blowroom_batch (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    batch_number    VARCHAR(50) UNIQUE NOT NULL,          -- BL-14030115-001
    order_id        BIGINT,                              -- ارتباط با سفارش
    machine_id      BIGINT NOT NULL,
    operator_id     BIGINT NOT NULL,
    shift_id        BIGINT NOT NULL,
    production_date DATE NOT NULL,
    -- پارامترهای تولید
    total_input_weight  DECIMAL(12,3) NOT NULL,          -- وزن کل ورودی (kg)
    output_weight       DECIMAL(12,3),                   -- وزن خروجی (kg)
    waste_weight        DECIMAL(10,3),                   -- وزن ضایعات (kg)
    waste_pct           DECIMAL(5,2),                    -- درصد ضایعات (محاسبه‌ای)
    blend_recipe        JSON,                            -- فرمول مخلوط (نسبت‌ها)
    -- وضعیت
    status          ENUM('in_progress','completed','cancelled') DEFAULT 'in_progress',
    started_at      DATETIME,
    completed_at    DATETIME,
    notes           TEXT,
    metadata        JSON,                                -- برای AI
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_date (production_date),
    INDEX idx_status (status),
    INDEX idx_order (order_id),
    FOREIGN KEY (machine_id) REFERENCES core_machine(id),
    FOREIGN KEY (operator_id) REFERENCES accounts_user(id),
    FOREIGN KEY (shift_id) REFERENCES core_shift(id),
    FOREIGN KEY (order_id) REFERENCES orders_order(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 5.2 blowroom_batchinput (ورودی‌های بچ حلاجی)
```sql
CREATE TABLE blowroom_batchinput (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    batch_id        BIGINT NOT NULL,
    fiber_stock_id  BIGINT NOT NULL,                     -- الیاف مصرفی از انبار
    weight_used     DECIMAL(12,3) NOT NULL,              -- وزن مصرفی (kg)
    percentage      DECIMAL(5,2),                        -- درصد در مخلوط
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_batch (batch_id),
    INDEX idx_fiber (fiber_stock_id),
    FOREIGN KEY (batch_id) REFERENCES blowroom_batch(id) ON DELETE CASCADE,
    FOREIGN KEY (fiber_stock_id) REFERENCES inventory_fiberstock(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 6. CARDING APP (کاردینگ)

### 6.1 carding_production (تولید کاردینگ)
```sql
CREATE TABLE carding_production (
    id                  BIGINT AUTO_INCREMENT PRIMARY KEY,
    batch_number        VARCHAR(50) UNIQUE NOT NULL,     -- CD-14030115-001
    blowroom_batch_id   BIGINT,                          -- بچ ورودی از حلاجی
    order_id            BIGINT,
    machine_id          BIGINT NOT NULL,
    operator_id         BIGINT NOT NULL,
    shift_id            BIGINT NOT NULL,
    production_date     DATE NOT NULL,
    -- پارامترهای فنی
    speed_rpm           DECIMAL(8,2),                    -- سرعت ماشین
    sliver_count        DECIMAL(8,3) NOT NULL,           -- نمره فتیله (نمره)
    sliver_weight_gperm DECIMAL(8,3),                    -- وزن فتیله (گرم بر متر)
    input_weight        DECIMAL(12,3),                   -- وزن ورودی (kg)
    output_weight       DECIMAL(12,3),                   -- وزن خروجی (kg)
    waste_weight        DECIMAL(10,3),                   -- ضایعات
    waste_pct           DECIMAL(5,2),
    -- نگهداری
    cleaning_time       TIME,                            -- زمان تمیزکاری
    last_cleaning_at    DATETIME,
    neps_count          INT,                             -- تعداد گره (کیفیت)
    -- وضعیت
    status              ENUM('in_progress','completed','quality_hold','cancelled') DEFAULT 'in_progress',
    started_at          DATETIME,
    completed_at        DATETIME,
    notes               TEXT,
    metadata            JSON,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_date (production_date),
    INDEX idx_machine (machine_id),
    INDEX idx_status (status),
    FOREIGN KEY (blowroom_batch_id) REFERENCES blowroom_batch(id),
    FOREIGN KEY (order_id) REFERENCES orders_order(id),
    FOREIGN KEY (machine_id) REFERENCES core_machine(id),
    FOREIGN KEY (operator_id) REFERENCES accounts_user(id),
    FOREIGN KEY (shift_id) REFERENCES core_shift(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 7. PASSAGE APP (پاساژ/کشش) ⚠️ بحرانی‌ترین ماژول

### 7.1 passage_production (تولید پاساژ)
```sql
CREATE TABLE passage_production (
    id                  BIGINT AUTO_INCREMENT PRIMARY KEY,
    batch_number        VARCHAR(50) UNIQUE NOT NULL,     -- PS-14030115-001
    passage_number      TINYINT NOT NULL DEFAULT 1,      -- شماره پاساژ (1=اول، 2=دوم)
    order_id            BIGINT,
    machine_id          BIGINT NOT NULL,
    operator_id         BIGINT NOT NULL,
    shift_id            BIGINT NOT NULL,
    production_date     DATE NOT NULL,
    -- پارامترهای فنی (حیاتی)
    num_inputs          TINYINT NOT NULL DEFAULT 6,      -- تعداد فتیله ورودی (6-8)
    draft_ratio         DECIMAL(8,3) NOT NULL,           -- نسبت کشش (مثلا 6.5)
    output_sliver_count DECIMAL(8,3) NOT NULL,           -- نمره فتیله خروجی
    output_weight_gperm DECIMAL(8,3),                    -- وزن فتیله خروجی (g/m)
    input_total_weight  DECIMAL(12,3),                   -- وزن کل ورودی
    output_weight       DECIMAL(12,3),                   -- وزن خروجی
    speed_mpm           DECIMAL(8,2),                    -- سرعت (متر بر دقیقه)
    evenness_cv         DECIMAL(5,2),                    -- CV% یکنواختی (برای AI)
    -- وضعیت
    status              ENUM('in_progress','completed','quality_hold','cancelled') DEFAULT 'in_progress',
    started_at          DATETIME,
    completed_at        DATETIME,
    notes               TEXT,
    metadata            JSON,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_date (production_date),
    INDEX idx_passage_num (passage_number),
    INDEX idx_status (status),
    FOREIGN KEY (order_id) REFERENCES orders_order(id),
    FOREIGN KEY (machine_id) REFERENCES core_machine(id),
    FOREIGN KEY (operator_id) REFERENCES accounts_user(id),
    FOREIGN KEY (shift_id) REFERENCES core_shift(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 7.2 passage_input (ورودی‌های پاساژ - ردیابی ادغام بچ) ⚠️ کلیدی
```sql
-- این جدول ردیابی می‌کند که هر بچ پاساژ از ترکیب کدام بچ‌های کاردینگ یا پاساژ قبلی ساخته شده
CREATE TABLE passage_input (
    id                  BIGINT AUTO_INCREMENT PRIMARY KEY,
    passage_prod_id     BIGINT NOT NULL,                 -- بچ پاساژ خروجی
    input_position      TINYINT NOT NULL,                -- جایگاه ورودی (1 تا 8)
    -- منبع ورودی (polymorphic: از کاردینگ یا پاساژ قبلی)
    source_type         ENUM('carding','passage') NOT NULL,
    source_id           BIGINT NOT NULL,                 -- FK به carding_production یا passage_production
    source_batch_number VARCHAR(50) NOT NULL,             -- شماره بچ مرجع (برای خوانایی)
    weight_used         DECIMAL(12,3),                   -- وزن مصرفی از این منبع
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_position (passage_prod_id, input_position),
    INDEX idx_source (source_type, source_id),
    FOREIGN KEY (passage_prod_id) REFERENCES passage_production(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 8. FINISHER APP (فینیشر)

### 8.1 finisher_production (تولید فینیشر)
```sql
CREATE TABLE finisher_production (
    id                  BIGINT AUTO_INCREMENT PRIMARY KEY,
    batch_number        VARCHAR(50) UNIQUE NOT NULL,     -- FN-14030115-001
    passage_prod_id     BIGINT,                          -- بچ ورودی از پاساژ
    order_id            BIGINT,
    machine_id          BIGINT NOT NULL,
    operator_id         BIGINT NOT NULL,
    shift_id            BIGINT NOT NULL,
    production_date     DATE NOT NULL,
    -- پارامترهای فنی
    draft_ratio         DECIMAL(8,3),                    -- نسبت کشش نهایی
    twist_tpm           DECIMAL(8,2),                    -- تاب اولیه (دور بر متر)
    output_sliver_count DECIMAL(8,3) NOT NULL,
    speed_mpm           DECIMAL(8,2),
    input_weight        DECIMAL(12,3),
    output_weight       DECIMAL(12,3),
    -- وضعیت
    status              ENUM('in_progress','completed','cancelled') DEFAULT 'in_progress',
    started_at          DATETIME,
    completed_at        DATETIME,
    notes               TEXT,
    metadata            JSON,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_date (production_date),
    INDEX idx_status (status),
    FOREIGN KEY (passage_prod_id) REFERENCES passage_production(id),
    FOREIGN KEY (order_id) REFERENCES orders_order(id),
    FOREIGN KEY (machine_id) REFERENCES core_machine(id),
    FOREIGN KEY (operator_id) REFERENCES accounts_user(id),
    FOREIGN KEY (shift_id) REFERENCES core_shift(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 9. SPINNING APP (رینگ)

### 9.1 spinning_production (تولید رینگ)
```sql
CREATE TABLE spinning_production (
    id                  BIGINT AUTO_INCREMENT PRIMARY KEY,
    batch_number        VARCHAR(50) UNIQUE NOT NULL,     -- RG-14030115-001
    finisher_prod_id    BIGINT,                          -- بچ ورودی از فینیشر
    order_id            BIGINT,
    machine_id          BIGINT NOT NULL,
    operator_id         BIGINT NOT NULL,
    shift_id            BIGINT NOT NULL,
    production_date     DATE NOT NULL,
    -- پارامترهای فنی رینگ
    spindle_speed_rpm   INT NOT NULL,                    -- سرعت دوک
    twist_tpm           DECIMAL(8,2) NOT NULL,           -- تاب (Taab) - دور بر متر
    twist_direction     ENUM('S','Z') DEFAULT 'Z',       -- جهت تاب
    yarn_count          DECIMAL(8,3) NOT NULL,           -- نمره نخ نهایی
    traveler_number     VARCHAR(20),                     -- شماره شیطانک
    traveler_type       VARCHAR(50),                     -- نوع شیطانک
    ring_diameter       DECIMAL(6,2),                    -- قطر رینگ (mm)
    -- تولید
    input_weight        DECIMAL(12,3),
    output_weight       DECIMAL(12,3),
    num_spindles_active INT,                             -- تعداد دوک فعال
    num_spindles_total  INT,                             -- تعداد کل دوک
    breakage_count      INT DEFAULT 0,                   -- تعداد پارگی
    efficiency_pct      DECIMAL(5,2),                    -- راندمان (برای AI/OEE)
    -- وضعیت
    status              ENUM('in_progress','completed','quality_hold','cancelled') DEFAULT 'in_progress',
    started_at          DATETIME,
    completed_at        DATETIME,
    notes               TEXT,
    metadata            JSON,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_date (production_date),
    INDEX idx_machine (machine_id),
    INDEX idx_status (status),
    FOREIGN KEY (finisher_prod_id) REFERENCES finisher_production(id),
    FOREIGN KEY (order_id) REFERENCES orders_order(id),
    FOREIGN KEY (machine_id) REFERENCES core_machine(id),
    FOREIGN KEY (operator_id) REFERENCES accounts_user(id),
    FOREIGN KEY (shift_id) REFERENCES core_shift(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 9.2 spinning_travelerreplacement (سیکل تعویض شیطانک)
```sql
CREATE TABLE spinning_travelerreplacement (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    machine_id      BIGINT NOT NULL,
    operator_id     BIGINT NOT NULL,
    replaced_at     DATETIME NOT NULL,
    old_traveler    VARCHAR(50),                         -- شیطانک قدیم
    new_traveler    VARCHAR(50) NOT NULL,                -- شیطانک جدید
    spindle_range   VARCHAR(50),                         -- بازه دوک‌ها (مثلا 1-240)
    reason          ENUM('scheduled','worn','breakage','quality') DEFAULT 'scheduled',
    running_hours   DECIMAL(8,2),                        -- ساعت کار تا تعویض
    next_due_at     DATETIME,                            -- زمان تعویض بعدی
    notes           TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_machine (machine_id),
    INDEX idx_next_due (next_due_at),                    -- برای هشدار PM
    FOREIGN KEY (machine_id) REFERENCES core_machine(id),
    FOREIGN KEY (operator_id) REFERENCES accounts_user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 10. DYEING APP (رنگرزی)

### 10.1 dyeing_batch (بچ رنگرزی)
```sql
CREATE TABLE dyeing_batch (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    batch_number    VARCHAR(50) UNIQUE NOT NULL,          -- DY-14030115-001
    order_id        BIGINT,
    color_shade_id  BIGINT NOT NULL,
    machine_id      BIGINT NOT NULL,                     -- دیگ رنگرزی
    operator_id     BIGINT NOT NULL,
    shift_id        BIGINT NOT NULL,
    production_date DATE NOT NULL,
    -- پارامترهای رنگرزی
    fiber_weight    DECIMAL(12,3) NOT NULL,              -- وزن الیاف (kg)
    liquor_ratio    DECIMAL(5,2),                        -- نسبت حمام
    temperature     DECIMAL(5,2),                        -- دمای حمام (°C)
    duration_min    INT,                                 -- مدت زمان (دقیقه)
    ph_value        DECIMAL(4,2),                        -- pH
    -- وضعیت
    status          ENUM('preparation','in_progress','cooling','drying','completed','failed') DEFAULT 'preparation',
    started_at      DATETIME,
    completed_at    DATETIME,
    quality_result  ENUM('pass','fail','conditional'),
    notes           TEXT,
    metadata        JSON,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_date (production_date),
    INDEX idx_status (status),
    FOREIGN KEY (order_id) REFERENCES orders_order(id),
    FOREIGN KEY (color_shade_id) REFERENCES orders_colorshade(id),
    FOREIGN KEY (machine_id) REFERENCES core_machine(id),
    FOREIGN KEY (operator_id) REFERENCES accounts_user(id),
    FOREIGN KEY (shift_id) REFERENCES core_shift(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 10.2 dyeing_chemicalusage (مصرف مواد شیمیایی رنگرزی)
```sql
CREATE TABLE dyeing_chemicalusage (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    dyeing_batch_id BIGINT NOT NULL,
    -- مواد مصرفی (یکی از سه نوع)
    material_type   ENUM('dye','chemical') NOT NULL,
    dye_stock_id    BIGINT,
    chemical_stock_id BIGINT,
    -- مقدار
    quantity_used   DECIMAL(12,3) NOT NULL,
    unit            VARCHAR(10) NOT NULL,
    step_name       VARCHAR(100),                        -- مرحله مصرف (شست‌وشو، رنگرزی، ...)
    sequence_order  TINYINT,                             -- ترتیب اضافه‌کردن
    notes           TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_batch (dyeing_batch_id),
    FOREIGN KEY (dyeing_batch_id) REFERENCES dyeing_batch(id) ON DELETE CASCADE,
    FOREIGN KEY (dye_stock_id) REFERENCES inventory_dyestock(id),
    FOREIGN KEY (chemical_stock_id) REFERENCES inventory_chemicalstock(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 10.3 dyeing_boilerlog (لاگ دیگ بخار)
```sql
CREATE TABLE dyeing_boilerlog (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    machine_id      BIGINT NOT NULL,                     -- دیگ بخار
    operator_id     BIGINT NOT NULL,
    log_date        DATE NOT NULL,
    shift_id        BIGINT NOT NULL,
    -- پارامترها
    pressure_bar    DECIMAL(6,2),                        -- فشار (بار)
    temperature_c   DECIMAL(6,2),                        -- دما
    water_level     DECIMAL(5,2),                        -- سطح آب (درصد)
    fuel_consumed   DECIMAL(10,3),                       -- مصرف سوخت (لیتر/متر مکعب)
    running_hours   DECIMAL(6,2),                        -- ساعت کار
    status          ENUM('running','idle','maintenance') DEFAULT 'running',
    notes           TEXT,
    metadata        JSON,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_machine_date (machine_id, log_date),
    FOREIGN KEY (machine_id) REFERENCES core_machine(id),
    FOREIGN KEY (operator_id) REFERENCES accounts_user(id),
    FOREIGN KEY (shift_id) REFERENCES core_shift(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 10.4 dyeing_dryerlog (لاگ خشک‌کن)
```sql
CREATE TABLE dyeing_dryerlog (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    machine_id      BIGINT NOT NULL,
    operator_id     BIGINT NOT NULL,
    dyeing_batch_id BIGINT,
    log_date        DATE NOT NULL,
    shift_id        BIGINT NOT NULL,
    temperature_c   DECIMAL(6,2),
    duration_min    INT,
    humidity_pct    DECIMAL(5,2),                        -- رطوبت خروجی
    status          ENUM('running','idle','maintenance') DEFAULT 'running',
    notes           TEXT,
    metadata        JSON,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_machine_date (machine_id, log_date),
    FOREIGN KEY (machine_id) REFERENCES core_machine(id),
    FOREIGN KEY (operator_id) REFERENCES accounts_user(id),
    FOREIGN KEY (dyeing_batch_id) REFERENCES dyeing_batch(id),
    FOREIGN KEY (shift_id) REFERENCES core_shift(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 11. MAINTENANCE APP (نگهداری و PM)

### 11.1 maintenance_schedule (برنامه سرویس)
```sql
CREATE TABLE maintenance_schedule (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    machine_id      BIGINT NOT NULL,
    maintenance_type ENUM('preventive','corrective','predictive','overhaul') NOT NULL,
    title           VARCHAR(200) NOT NULL,
    description     TEXT,
    frequency       ENUM('daily','weekly','biweekly','monthly','quarterly','semi_annual','annual','custom') NOT NULL,
    custom_days     INT,                                 -- تعداد روز برای custom
    last_done_at    DATETIME,
    next_due_at     DATETIME NOT NULL,
    assigned_to_id  BIGINT,
    priority        ENUM('low','medium','high','critical') DEFAULT 'medium',
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_next_due (next_due_at),
    INDEX idx_machine (machine_id),
    INDEX idx_assigned (assigned_to_id),
    INDEX idx_overdue (is_active, next_due_at),          -- برای هشدار
    FOREIGN KEY (machine_id) REFERENCES core_machine(id),
    FOREIGN KEY (assigned_to_id) REFERENCES accounts_user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 11.2 maintenance_workorder (دستور کار تعمیرات)
```sql
CREATE TABLE maintenance_workorder (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    wo_number       VARCHAR(20) UNIQUE NOT NULL,         -- WO-14030115-001
    schedule_id     BIGINT,                              -- ارتباط با برنامه PM (اختیاری)
    machine_id      BIGINT NOT NULL,
    title           VARCHAR(200) NOT NULL,
    description     TEXT,
    wo_type         ENUM('preventive','corrective','emergency') NOT NULL,
    priority        ENUM('low','medium','high','critical') DEFAULT 'medium',
    reported_by_id  BIGINT NOT NULL,
    assigned_to_id  BIGINT,
    status          ENUM('open','in_progress','waiting_parts','completed','cancelled') DEFAULT 'open',
    started_at      DATETIME,
    completed_at    DATETIME,
    downtime_min    INT,                                 -- مدت توقف (دقیقه)
    cost_parts      DECIMAL(15,0) DEFAULT 0,             -- هزینه قطعات
    cost_labor      DECIMAL(15,0) DEFAULT 0,             -- هزینه دستمزد
    notes           TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_machine (machine_id),
    INDEX idx_status (status),
    INDEX idx_priority_status (priority, status),
    FOREIGN KEY (schedule_id) REFERENCES maintenance_schedule(id),
    FOREIGN KEY (machine_id) REFERENCES core_machine(id),
    FOREIGN KEY (reported_by_id) REFERENCES accounts_user(id),
    FOREIGN KEY (assigned_to_id) REFERENCES accounts_user(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 11.3 maintenance_downtimelog (لاگ توقفات)
```sql
CREATE TABLE maintenance_downtimelog (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    machine_id      BIGINT NOT NULL,
    work_order_id   BIGINT,
    operator_id     BIGINT NOT NULL,
    shift_id        BIGINT NOT NULL,
    start_time      DATETIME NOT NULL,
    end_time        DATETIME,
    duration_min    INT,                                 -- محاسبه‌ای
    reason_category ENUM('mechanical','electrical','material','operator','quality','planned','other') NOT NULL,
    reason_detail   VARCHAR(500) NOT NULL,               -- جزئیات دلیل توقف
    production_loss DECIMAL(12,3),                       -- تولید از دست رفته (kg)
    notes           TEXT,
    metadata        JSON,                                -- برای AI/Predictive
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_machine_date (machine_id, start_time),
    INDEX idx_reason (reason_category),
    INDEX idx_shift (shift_id, start_time),              -- تحلیل شیفتی
    FOREIGN KEY (machine_id) REFERENCES core_machine(id),
    FOREIGN KEY (work_order_id) REFERENCES maintenance_workorder(id),
    FOREIGN KEY (operator_id) REFERENCES accounts_user(id),
    FOREIGN KEY (shift_id) REFERENCES core_shift(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 11.4 maintenance_machineservicedate (تاریخ سرویس ماشین‌آلات)
```sql
CREATE TABLE maintenance_machineservicedate (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    machine_id      BIGINT NOT NULL,
    service_type    VARCHAR(100) NOT NULL,               -- نوع سرویس
    service_date    DATE NOT NULL,
    next_service    DATE,
    performed_by    VARCHAR(200),                        -- سرویس‌کار
    cost            DECIMAL(15,0) DEFAULT 0,
    parts_replaced  JSON,                                -- قطعات تعویض شده
    notes           TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_machine_date (machine_id, service_date),
    INDEX idx_next (next_service),
    FOREIGN KEY (machine_id) REFERENCES core_machine(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 12. فیلدهای آماده AI (AI-Ready Fields)

جداول زیر فیلد `metadata JSON` دارند که در فاز AI پر خواهند شد:

| جدول | کاربرد AI |
|------|----------|
| `carding_production.metadata` | تحلیل ارتباط سرعت/نمره با کیفیت |
| `passage_production.metadata` | بهینه‌سازی نسبت کشش |
| `spinning_production.metadata` | پیش‌بینی پارگی نخ |
| `spinning_production.efficiency_pct` | محاسبه OEE |
| `spinning_production.breakage_count` | تحلیل الگوی پارگی |
| `maintenance_downtimelog.metadata` | Predictive Maintenance |
| `dyeing_batch.metadata` | بهینه‌سازی فرمول رنگ |
| `core_machine.specs` | پروفایل عملکرد ماشین |

---

## 13. نمودار روابط (Relationship Summary)

```
inventory_fiberstock ──┐
                       ├──► blowroom_batch ──► carding_production ──┐
inventory_fiberstock ──┘                                            │
                                                                    ├──► passage_production ──► finisher_production ──► spinning_production
                                                                    │        ▲                                               │
                                                              passage_input  │                                               │
                                                        (Multi-Input Link)   │                                               ▼
                                                                             │                                         [نخ نهایی]
                                                              passage_production (Passage 2)
                                                              
orders_order ─────────────────────────────────────────────────────────────────────────────────────────────►  tracks all production stages
orders_colorshade ──► orders_colorapprovalhistory
orders_colorshade ──► dyeing_batch ──► dyeing_chemicalusage ──► inventory_dyestock / inventory_chemicalstock

core_machine ──► maintenance_schedule ──► maintenance_workorder
core_machine ──► maintenance_downtimelog
core_machine ──► maintenance_machineservicedate
core_machine ──► spinning_travelerreplacement
```

---

**مجموع جداول: 27 جدول**
**مجموع ایندکس‌ها: 60+ ایندکس بهینه**
**پوشش: کل زنجیره تولید + انبار + سفارشات + رنگرزی + نگهداری + آماده AI**
