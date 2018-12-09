pragma solidity ^0.5.0;
contract Store{    
    struct  Estate {
        uint estate_id;
        address owner;
        string info;
        uint squere;
        uint useful_squere;
        bool present_status;
        bool sale_status;
        bool pledge_status;}
    struct Present {
        uint estate_id;
        address address_from;
        address address_to;
        uint deadline;}
    struct Sale {
        uint estate_id;
        address owner;
        uint price;
        uint time;
        uint deadline;
        address payable[] customers;
        uint[] prices;}
    struct Pledge {
        uint estate_id;
        address payable owner_address;
        address payable money_address;
        uint money;
        uint time;
        uint deadline;
        bool p_status;}
    Estate[] estates;
    Present[] presents;
    Sale[] sales;
    Pledge[] pledges;
    address admin = 0x2F9Ef54732FDCc38331451F866a344333e82d9D2;
    address payable default_address = 0x0000000000000000000000000000000000000000;   
    modifier isOwner(uint estate_id) {
        require(msg.sender == estates[estate_id].owner);
        require(estates[estate_id].present_status == false);
        require(estates[estate_id].sale_status == false);
        require(estates[estate_id].pledge_status == false);
        _;}   
    modifier isAdmin {
        require(msg.sender == admin);
        _;}  
    //Admin's function    
    //Создать объект собственности
    function create_estate(address owner, string memory info, uint squere, uint useful_squere) public isAdmin {
        estates.push(Estate(estates.length, owner, info, squere, useful_squere, false, false, false));}    
    function get_estates_number() public view returns(uint) {
        return estates.length;}   
    function get_estates(uint estate_number) public view returns(uint, address, string memory, uint, uint) {
		return(estates[estate_number].estate_id, estates[estate_number].owner, estates[estate_number].info, estates[estate_number].squere, estates[estate_number].useful_squere);}
    function get_estates_statuses(uint estate_number) public view returns(bool, bool, bool) {
        return(estates[estate_number].present_status, estates[estate_number].sale_status, estates[estate_number].pledge_status);}
	function get_presents_number() public view returns(uint) {
        return presents.length;}
    function get_presents(uint present_number) public view returns(uint, address, address, uint) {
        return(presents[present_number].estate_id, presents[present_number].address_from, presents[present_number].address_to, presents[present_number].deadline);}   
    function get_presentID_by_estateID(uint estateID) public view returns(uint) {
        for(uint i=0; i<presents.length; i++) {
			if(estateID == presents[i].estate_id && presents[i].address_from != default_address) {
                return(i);}}}
    // Создать предложение подарка
    function create_present(uint estate_id, address address_to, uint time) public isOwner(estate_id) {
        require(msg.sender != address_to);
        presents.push(Present(estate_id, msg.sender, address_to, block.timestamp + time));
        estates[estate_id].present_status = true;}    
    // Отменить свой подарок(доступна до принятие подарка адресатом)
    function cancel_present(uint estateID) payable public {
        uint present_number = get_presentID_by_estateID(estateID);
        require(msg.sender == presents[present_number].address_from);
        require(presents[present_number].deadline >= block.timestamp);
        estates[presents[present_number].estate_id].present_status = false;
        delete presents[present_number];}    
    // Принять подарок
    function confirm_present(uint estateID) payable public {
        uint present_number = get_presentID_by_estateID(estateID);
        require(msg.sender == presents[present_number].address_to);
        require(presents[present_number].deadline >= block.timestamp);
        estates[presents[present_number].estate_id].owner = presents[present_number].address_to;
        estates[presents[present_number].estate_id].present_status = false;
        delete presents[present_number];}   
    // Удалить подарок, т.к. срок истек
    function present_time_out(uint estateID) public isAdmin {
        uint present_number = get_presentID_by_estateID(estateID);
        require(presents[present_number].deadline < block.timestamp, "1");
        estates[presents[present_number].estate_id].present_status = false;
        delete presents[present_number];}
    function get_sales_number() public view returns(uint) {
        return sales.length;}
    function get_sales(uint sale_number) public view returns(uint, address, uint, uint, uint, address payable[] memory, uint[] memory prices) {
        return(sales[sale_number].estate_id, sales[sale_number].owner, sales[sale_number].price, sales[sale_number].time, sales[sale_number].deadline, sales[sale_number].customers, sales[sale_number].prices);}   
    function get_saleID_by_estateID(uint estateID) public view returns(uint) {
        for(uint i=0; i<sales.length; i++) {
            if(estateID == sales[i].estate_id && sales[i].owner != default_address) {
                return(i);}}}
    // Разместить объявление о продаже
    function create_sale(uint estate_id, uint price, uint date) public isOwner(estate_id) {
       address payable[] memory customers;
       uint[] memory prices;
       sales.push(Sale(estate_id, msg.sender, price, date, date + now, customers, prices));
       estates[estate_id].sale_status = true;}    
    // Отменить объявление о продаже и вернуть деньги всем, кто успел внести
    function cancel_sale(uint estateID) public  {
        uint sale_number = get_saleID_by_estateID(estateID);
        require(msg.sender == sales[sale_number].owner);
        for (uint i = 0; i < sales[sale_number].customers.length; i++){
            (sales[sale_number].customers[i]).transfer(sales[sale_number].prices[i]);}
        estates[sales[sale_number].estate_id].sale_status = false;
        delete sales[sale_number];}  
    // Выбрать чтобы купить
    function check_to_buy(uint estateID) public payable {
        uint sale_number = get_saleID_by_estateID(estateID);
        require(msg.sender != sales[sale_number].owner);
        require(msg.value >= sales[sale_number].price);
        require(now <= sales[sale_number].deadline);
        uint status = 0;
        for (uint i=0; i < sales[sale_number].customers.length; i++) {
            if (sales[sale_number].customers[i] == msg.sender) {
                status = 1;
                break;}}
        require(status == 0);
        sales[sale_number].customers.push(msg.sender);
        sales[sale_number].prices.push(msg.value);}  
    // Отменить выбор покупки
    function cancel_to_buy(uint estateID) public payable {
        uint sale_number = get_saleID_by_estateID(estateID);
        for (uint i=0; i<sales[sale_number].customers.length; i++){
            if (sales[sale_number].customers[i] == msg.sender){
                msg.sender.transfer(sales[sale_number].prices[i]);
                delete sales[sale_number].customers[i];
                delete sales[sale_number].prices[i];}}}   
    // Подтвердить продажу и вернуть деньги остальным
    function confirm_sale(uint estateID, uint sale_to) public payable {
        uint sale_number = get_saleID_by_estateID(estateID);
        require(msg.sender == sales[sale_number].owner);
        require(now <=  sales[sale_number].deadline);
        estates[sales[sale_number].estate_id].owner = sales[sale_number].customers[sale_to];
        msg.sender.transfer(sales[sale_number].prices[sale_to]);
        for (uint i=0; i<sales[sale_number].customers.length; i++){
            if (i != sale_to) {
                sales[sale_number].customers[i].transfer(sales[sale_number].prices[i]);}}
        estates[sales[sale_number].estate_id].sale_status = false;
        delete sales[sale_number];}
    // Удалить продажу, т.к. время истекло 
    function sale_time_out(uint estateID) public isAdmin {
        uint sale_number = get_saleID_by_estateID(estateID);
        require(sales[sale_number].deadline < now);
        for (uint i = 0; i < sales[sale_number].customers.length; i++){
            (sales[sale_number].customers[i]).transfer(sales[sale_number].prices[i]);}
        estates[sales[sale_number].estate_id].sale_status = false;
        delete sales[sale_number];}
	    function get_pledges_number() public view returns(uint) {
        return pledges.length;}  
    function get_pledges(uint pledge_number) public view returns(uint, address, address, uint, uint, uint, bool) {
        return(pledges[pledge_number].estate_id, pledges[pledge_number].owner_address, pledges[pledge_number].money_address, pledges[pledge_number].money, pledges[pledge_number].time, pledges[pledge_number].deadline, pledges[pledge_number].p_status);}          
    function get_pledgeID_by_estateID(uint estateID) public view returns(uint) {
        for(uint i=0; i<pledges.length; i++) {
            if(estateID == pledges[i].estate_id && pledges[i].owner_address != default_address) {
                return(i);}}}            
    //Создать объявление о залоге
    function create_pledge(uint estate_id, uint money, uint time) public isOwner(estate_id) {
        pledges.push(Pledge(estate_id, msg.sender, default_address, money, time, 0, false));
        estates[estate_id].pledge_status = true;}   
    // Отменить свое предложение о залоге и вернуть деньги залогодавателю
    function cancel_pledge(uint estateID) public payable {
        uint pledge_number = get_pledgeID_by_estateID(estateID);
        require(msg.sender == pledges[pledge_number].owner_address);
        if (pledges[pledge_number].money_address != default_address) {
            pledges[pledge_number].money_address.transfer(pledges[pledge_number].money);}
        estates[pledges[pledge_number].estate_id].pledge_status = false;
        delete pledges[pledge_number];}   
    // Выбрать чтобы выдать залог
    function check_to_pledge(uint estateID) public payable {
        uint pledge_number = get_pledgeID_by_estateID(estateID);
        require(msg.value == pledges[pledge_number].money);
        require(msg.sender != pledges[pledge_number].owner_address);
        pledges[pledge_number].money_address = msg.sender;}    
    // Отменить предложенный залог
    function cancel_to_pledge(uint estateID) public payable {
        uint pledge_number = get_pledgeID_by_estateID(estateID);
        require(msg.sender == pledges[pledge_number].money_address);
        msg.sender.transfer(pledges[pledge_number].money);
        pledges[pledge_number].money_address = default_address;}   
    // Принять деньги в залог, начинается отсчет времени
    function confirm_pledge(uint estateID) public {
        uint pledge_number = get_pledgeID_by_estateID(estateID);
        require(msg.sender == pledges[pledge_number].owner_address);
        pledges[pledge_number].deadline = pledges[pledge_number].time + now;
        pledges[pledge_number].owner_address.transfer(pledges[pledge_number].money);}
    //Отказаться от предложения
    function refuse_pledge(uint estateID) payable public {
        uint pledge_number = get_pledgeID_by_estateID(estateID);
        require(msg.sender == pledges[pledge_number].owner_address);
        pledges[pledge_number].money_address.transfer(pledges[pledge_number].money);
        pledges[pledge_number].money_address = default_address;}    
    // Вернуть деньги, полученные в залог
    function finish_pledge(uint estateID) payable public {
        uint pledge_number = get_pledgeID_by_estateID(estateID);
        require(msg.value == pledges[pledge_number].money);
        require(msg.sender == pledges[pledge_number].owner_address);
        require(pledges[pledge_number].deadline >= now);
        pledges[pledge_number].money_address.transfer(pledges[pledge_number].money);
        estates[pledges[pledge_number].estate_id].pledge_status = false;
        delete pledges[pledge_number];}  
    // Завершить залог по истечению времени
    function pledge_time_out(uint estateID) payable public isAdmin {
        uint pledge_number = get_pledgeID_by_estateID(estateID);
        require(pledges[pledge_number].deadline < now);
        estates[pledges[pledge_number].estate_id].owner = pledges[pledge_number].money_address;
        estates[pledges[pledge_number].estate_id].pledge_status = false;
        delete pledges[pledge_number];}}