export default function ServicesSection() {
  const services = [
    { title: 'Web Browsers' },
    { title: 'Office Suites' },
    { title: 'Messaging' },
    { title: 'Mail' },
  ];

  return (
    <section style={{
      padding: '0px 48px',
      backgroundColor: '#FFFFFF'
    }}>
      <div className="flex flex-row flex-wrap justify-between gap-8">
        {services.map((service, index) => (
          <div 
            key={index}
            className=" p-8 bg-white hover:bg-lime hover:text-black transition-colors duration-300"
          >
            <h3 className="text-xl font-bold  text-black">{service.title}</h3>
          </div>
        ))}
      </div>
    </section>
  );
}
