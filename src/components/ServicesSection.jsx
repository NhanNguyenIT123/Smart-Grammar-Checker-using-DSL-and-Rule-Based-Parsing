export default function ServicesSection() {
  const services = [
    { title: 'Web Browsers', icon: '🌐' },
    { title: 'Office Suites', icon: '📄' },
    { title: 'Messaging', icon: '💬' },
    { title: 'Mail', icon: '📧' },
  ];

  return (
    <section className="px-8 py-20 bg-light-gray">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {services.map((service, index) => (
          <div 
            key={index}
            className="border-2 border-black p-8 bg-white hover:bg-lime hover:text-black transition-colors duration-300"
          >
            <div className="text-4xl mb-4">{service.icon}</div>
            <h3 className="text-xl font-bold text-black">{service.title}</h3>
          </div>
        ))}
      </div>
    </section>
  );
}
